from sqlalchemy.orm import Session

from app.models.telemetry import TelemetryReadingModel
from app.schemas.telemetry import TelemetryReading


def save_telemetry(
    db: Session,
    telemetry: TelemetryReading
) -> TelemetryReadingModel:
    """
    Save one validated telemetry reading to PostgreSQL.
    """

    db_reading = TelemetryReadingModel(
        timestamp=telemetry.timestamp,
        voltage=telemetry.voltage,
        current=telemetry.current,
        active_power=telemetry.active_power,
        reactive_power=telemetry.reactive_power,
        apparent_power=telemetry.apparent_power,
        power_factor=telemetry.power_factor,
        frequency=telemetry.frequency,
        energy=telemetry.energy,
        demand=telemetry.demand,
        meter_id=telemetry.meter_id,
    )

    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)

    return db_reading