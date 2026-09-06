
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.schemas.telemetry import (
    TelemetryReading,
    MeterStatusResponse
)

from app.services.meter_service import (
    MeterService,
    get_meter_service
)

from app.services.energy_analysis_service import (
    analyze_energy
)

from app.services.llm_service import (
    generate_llm_response
)

from app.database.session import get_db
from app.models.telemetry import TelemetryReadingModel


router = APIRouter(
    prefix="/api/meter",
    tags=["Smart Meter"]
)


# ==========================================================
# SIMPLE CHAT MEMORY
# ==========================================================
#
# Keeps the most recent conversation for the local
# development chatbot.
#
# This allows:
#
# User:
# "If I need to use 760kg load what might the current be?"
#
# User:
# "yeah"
#
# The assistant can understand what "yeah" refers to.
#
# ==========================================================

conversation_history = []


# ==========================================================
# CURRENT TELEMETRY
# ==========================================================

@router.get(
    "/current",
    response_model=TelemetryReading,
    summary="Get Current Telemetry Reading",
    description=(
        "Returns latest 3-phase electrical telemetry readings "
        "from the configured smart meter connector."
    )
)
def get_current_telemetry(
    db: Session = Depends(get_db),
    meter_service: MeterService = Depends(get_meter_service)
) -> TelemetryReading:

    """
    Returns real-time electrical telemetry metrics
    and saves the reading to PostgreSQL.
    """

    return meter_service.get_current_telemetry(db)


# ==========================================================
# METER STATUS
# ==========================================================

@router.get(
    "/status",
    response_model=MeterStatusResponse,
    summary="Get Smart Meter Connector Status",
    description=(
        "Returns connection state and active hardware/mock "
        "connector details."
    )
)
def get_meter_status(
    meter_service: MeterService = Depends(get_meter_service)
) -> MeterStatusResponse:

    """
    Returns smart meter connector connection state
    and connector model information.
    """

    return meter_service.get_meter_status()


# ==========================================================
# TELEMETRY HISTORY
# ==========================================================

@router.get(
    "/history",
    response_model=list[TelemetryReading],
    summary="Get Telemetry History",
    description=(
        "Returns previously stored electrical telemetry "
        "readings from PostgreSQL."
    )
)
def get_telemetry_history(
    db: Session = Depends(get_db)
) -> list[TelemetryReading]:

    """
    Returns stored telemetry readings from PostgreSQL,
    newest readings first.
    """

    readings = (
        db.query(TelemetryReadingModel)
        .order_by(
            TelemetryReadingModel.timestamp.desc()
        )
        .all()
    )

    return [
        TelemetryReading(
            timestamp=reading.timestamp.isoformat(),
            voltage=reading.voltage,
            current=reading.current,
            active_power=reading.active_power,
            reactive_power=reading.reactive_power,
            apparent_power=reading.apparent_power,
            power_factor=reading.power_factor,
            frequency=reading.frequency,
            energy=reading.energy,
            demand=reading.demand,
            meter_id=reading.meter_id,
        )
        for reading in readings
    ]


# ==========================================================
# ENERGY ANALYSIS + AI CHATBOT
# ==========================================================

@router.get(
    "/analysis",
    summary="Analyze Energy Data",
    description=(
        "Analyzes recent telemetry and generates an AI "
        "response using the local Ollama LLM."
    )
)
def get_energy_analysis(
    question: str = Query(
        default="What is the current energy system status?",
        description="User question for the AI Energy Assistant."
    ),
    db: Session = Depends(get_db)
):

    """
    Analyzes the latest stored telemetry and recent
    historical readings.

    The endpoint:

    1. Reads existing telemetry from PostgreSQL.
    2. Performs trusted rule-based energy analysis.
    3. Sends the user's question, telemetry,
       analysis and conversation history to Ollama.
    4. Returns both analysis and AI response.

    IMPORTANT:

    This endpoint does NOT request a new meter reading.
    """

    global conversation_history

    # ======================================================
    # GET HISTORICAL READINGS
    # ======================================================

    historical_readings = (
        db.query(TelemetryReadingModel)
        .order_by(
            TelemetryReadingModel.timestamp.desc()
        )
        .limit(20)
        .all()
    )

    # ======================================================
    # NO DATA
    # ======================================================

    if not historical_readings:

        analysis = {
            "overall_status": "No Data",

            "findings": [],

            "trends": [
                {
                    "parameter": "Active Power Trend",
                    "status": "Insufficient Data",
                    "message": (
                        "No telemetry readings are currently "
                        "available in PostgreSQL."
                    )
                }
            ]
        }

        ai_response = generate_llm_response(
            question,
            analysis,
            None,
            conversation_history
        )

        conversation_history.append(
            {
                "user": question,
                "assistant": ai_response
            }
        )

        conversation_history = conversation_history[-6:]

        analysis["llm_response"] = ai_response

        return analysis

    # ======================================================
    # LATEST TELEMETRY
    # ======================================================

    latest_reading = historical_readings[0]

    telemetry = TelemetryReading(
        timestamp=latest_reading.timestamp.isoformat(),
        voltage=latest_reading.voltage,
        current=latest_reading.current,
        active_power=latest_reading.active_power,
        reactive_power=latest_reading.reactive_power,
        apparent_power=latest_reading.apparent_power,
        power_factor=latest_reading.power_factor,
        frequency=latest_reading.frequency,
        energy=latest_reading.energy,
        demand=latest_reading.demand,
        meter_id=latest_reading.meter_id,
    )

    # ======================================================
    # TRUSTED ENERGY ANALYSIS
    # ======================================================

    analysis = analyze_energy(
        telemetry,
        historical_readings
    )

    # ======================================================
    # LOCAL LLM
    # ======================================================

    ai_response = generate_llm_response(
        question,
        analysis,
        telemetry,
        conversation_history
    )

    # ======================================================
    # SAVE CONVERSATION
    # ======================================================

    conversation_history.append(
        {
            "user": question,
            "assistant": ai_response
        }
    )

    # Keep only recent conversation
    conversation_history = conversation_history[-6:]

    # ======================================================
    # RETURN RESPONSE
    # ======================================================

    analysis["llm_response"] = ai_response

    return analysis

