
import re
import os

from dotenv import load_dotenv
from google import genai


# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv("backend/.env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = "gemini-3.6-flash"


# ==========================================================
# GEMINI CLIENT
# ==========================================================

client = None

if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)


# ==========================================================
# QUESTION NORMALIZATION
# ==========================================================

def normalize_question(question: str) -> str:
    """
    Normalize common chat abbreviations and spelling mistakes.
    """

    q = question.lower().strip()

    replacements = {
        "wt": "what",
        "wht": "what",
        "wat": "what",
        "whats": "what is",
        "pls": "please",
        "plz": "please",
        "abt": "about",
        "hw": "how",
        "u": "you",
        "ur": "your",
        "pf": "power factor",
    }

    words = q.split()

    normalized_words = [
        replacements.get(word, word)
        for word in words
    ]

    q = " ".join(normalized_words)

    spelling_corrections = {
        "currnet": "current",
        "curent": "current",
        "currrent": "current",
        "volatge": "voltage",
        "voltge": "voltage",
        "volatage": "voltage",
        "powre": "power",
        "pwer": "power",
        "reactve": "reactive",
        "reactiv": "reactive",
        "apparant": "apparent",
        "apparentt": "apparent",
        "frequncy": "frequency",
        "frequeny": "frequency",
        "energry": "energy",
        "demad": "demand",
    }

    words = q.split()

    corrected_words = [
        spelling_corrections.get(word, word)
        for word in words
    ]

    q = " ".join(corrected_words)

    q = re.sub(r"[?!.,]+", "", q)
    q = re.sub(r"\s+", " ", q).strip()

    return q


# ==========================================================
# EXACT MEASUREMENT QUESTION DETECTION
# ==========================================================

def _is_exact_measurement_question(
    question: str,
    parameter: str
) -> bool:

    q = normalize_question(question)

    patterns = {

        "current": [
            r"^current$",
            r"^what is current$",
            r"^what is the current$",
            r"^what is current reading$",
            r"^what is the current reading$",
            r"^what is present current$",
            r"^what is the present current$",
            r"^what is current now$",
            r"^what is the current now$",
            r"^tell me current$",
            r"^tell me the current$",
            r"^show me current$",
            r"^show me the current$",
            r"^give me current$",
            r"^give me the current$",
            r"^how much current is flowing$",
            r"^how much current is being drawn$",
            r"^how many amps are flowing$",
            r"^how many amps$",
            r"^what are the amps$",
        ],

        "voltage": [
            r"^voltage$",
            r"^what is voltage$",
            r"^what is the voltage$",
            r"^what is voltage reading$",
            r"^what is the voltage reading$",
            r"^what is present voltage$",
            r"^what is the present voltage$",
            r"^what is voltage now$",
            r"^what is the voltage now$",
            r"^tell me voltage$",
            r"^tell me the voltage$",
            r"^show me voltage$",
            r"^show me the voltage$",
            r"^give me voltage$",
            r"^give me the voltage$",
        ],

        "active_power": [
            r"^active power$",
            r"^what is active power$",
            r"^what is the active power$",
            r"^what is active power reading$",
            r"^what is the active power reading$",
            r"^tell me active power$",
            r"^tell me the active power$",
            r"^show me active power$",
            r"^show me the active power$",
            r"^give me active power$",
            r"^give me the active power$",
        ],

        "reactive_power": [
            r"^reactive power$",
            r"^what is reactive power$",
            r"^what is the reactive power$",
            r"^what is reactive power reading$",
            r"^what is the reactive power reading$",
            r"^tell me reactive power$",
            r"^tell me the reactive power$",
            r"^show me reactive power$",
            r"^show me the reactive power$",
            r"^give me reactive power$",
            r"^give me the reactive power$",
        ],

        "apparent_power": [
            r"^apparent power$",
            r"^what is apparent power$",
            r"^what is the apparent power$",
            r"^what is apparent power reading$",
            r"^what is the apparent power reading$",
            r"^tell me apparent power$",
            r"^tell me the apparent power$",
            r"^show me apparent power$",
            r"^show me the apparent power$",
            r"^give me apparent power$",
            r"^give me the apparent power$",
        ],

        "power_factor": [
            r"^power factor$",
            r"^what is power factor$",
            r"^what is the power factor$",
            r"^what is power factor reading$",
            r"^what is the power factor reading$",
            r"^tell me power factor$",
            r"^tell me the power factor$",
            r"^show me power factor$",
            r"^show me the power factor$",
            r"^give me power factor$",
            r"^give me the power factor$",
        ],

        "frequency": [
            r"^frequency$",
            r"^what is frequency$",
            r"^what is the frequency$",
            r"^what is frequency reading$",
            r"^what is the frequency reading$",
            r"^tell me frequency$",
            r"^tell me the frequency$",
            r"^show me frequency$",
            r"^show me the frequency$",
            r"^give me frequency$",
            r"^give me the frequency$",
        ],

        "energy": [
            r"^energy$",
            r"^what is energy$",
            r"^what is the energy$",
            r"^energy consumption$",
            r"^what is energy consumption$",
            r"^what is the energy consumption$",
            r"^what is energy reading$",
            r"^what is the energy reading$",
            r"^how much energy was consumed$",
            r"^how much energy is consumed$",
            r"^tell me energy consumption$",
            r"^tell me the energy consumption$",
            r"^show me energy consumption$",
            r"^show me the energy consumption$",
        ],

        "demand": [
            r"^demand$",
            r"^what is demand$",
            r"^what is the demand$",
            r"^power demand$",
            r"^what is power demand$",
            r"^what is the power demand$",
            r"^what is demand reading$",
            r"^what is the demand reading$",
            r"^tell me demand$",
            r"^tell me the demand$",
            r"^show me demand$",
            r"^show me the demand$",
        ],
    }

    parameter_patterns = patterns.get(parameter, [])

    return any(
        re.fullmatch(pattern, q)
        for pattern in parameter_patterns
    )


# ==========================================================
# FOLLOW-UP QUESTION DETECTION
# ==========================================================

def _is_follow_up_question(question: str) -> bool:
    """
    Detect very short follow-up messages.
    """

    q = normalize_question(question)

    follow_ups = {
        "yeah",
        "yes",
        "yep",
        "yup",
        "ok",
        "okay",
        "sure",
        "continue",
        "go ahead",
        "then",
        "so",
        "correct",
        "right",
        "yes please",
        "okay please",
    }

    return q in follow_ups


# ==========================================================
# LOAD + CURRENT QUESTION DETECTION
# ==========================================================

def _looks_like_load_question(question: str) -> bool:
    """
    Detect questions involving physical load/mass.
    """

    q = normalize_question(question)

    load_words = [
        "kg",
        "kilogram",
        "kilograms",
        "load",
        "weight",
        "motor",
        "lifting",
        "lift",
    ]

    current_words = [
        "current",
        "amp",
        "amps",
        "amperes",
    ]

    has_load_word = any(
        word in q
        for word in load_words
    )

    has_current_word = any(
        word in q
        for word in current_words
    )

    return has_load_word and has_current_word


# ==========================================================
# MAIN GEMINI RESPONSE FUNCTION
# ==========================================================

def generate_llm_response(
    user_question: str,
    analysis: dict,
    telemetry=None,
    conversation_history=None
) -> str:

    """
    Hybrid AI Energy Monitoring Assistant.

    Uses:
    - deterministic logic for trusted meter readings
    - deterministic engineering safety logic
    - Gemini for explanations, analysis, trends and conversation
    """

    original_question = user_question.strip()

    normalized_question = normalize_question(
        original_question
    )

    if conversation_history is None:
        conversation_history = []

    # ======================================================
    # DIRECT TELEMETRY QUESTIONS
    # ======================================================

    if telemetry is not None:

        if _is_exact_measurement_question(
            normalized_question,
            "current"
        ):
            return (
                f"The current measured by the meter is "
                f"{telemetry.current} A."
            )

        if _is_exact_measurement_question(
            normalized_question,
            "voltage"
        ):
            return (
                f"The voltage measured by the meter is "
                f"{telemetry.voltage} V."
            )

        if _is_exact_measurement_question(
            normalized_question,
            "active_power"
        ):
            return (
                f"The active power measured by the meter is "
                f"{telemetry.active_power} kW."
            )

        if _is_exact_measurement_question(
            normalized_question,
            "reactive_power"
        ):
            return (
                f"The reactive power measured by the meter is "
                f"{telemetry.reactive_power} kVAR."
            )

        if _is_exact_measurement_question(
            normalized_question,
            "apparent_power"
        ):
            return (
                f"The apparent power measured by the meter is "
                f"{telemetry.apparent_power} kVA."
            )

        if _is_exact_measurement_question(
            normalized_question,
            "power_factor"
        ):
            return (
                f"The current power factor measured by the meter is "
                f"{telemetry.power_factor}."
            )

        if _is_exact_measurement_question(
            normalized_question,
            "frequency"
        ):
            return (
                f"The frequency measured by the meter is "
                f"{telemetry.frequency} Hz."
            )

        if _is_exact_measurement_question(
            normalized_question,
            "energy"
        ):
            return (
                f"The recorded energy consumption is "
                f"{telemetry.energy} kWh."
            )

        if _is_exact_measurement_question(
            normalized_question,
            "demand"
        ):
            return (
                f"The recorded demand is "
                f"{telemetry.demand} kW."
            )

    # ======================================================
    # SPECIAL CASE: LOAD + CURRENT
    # ======================================================

    if _looks_like_load_question(normalized_question):

        return (
            "The current required for a load cannot be determined "
            "from the load in kilograms alone.\n\n"
            "If you mean an electrical motor/load, I need information "
            "such as the supply voltage, motor power, power factor, "
            "efficiency, and whether the supply is single-phase or "
            "three-phase.\n\n"
            "For a three-phase motor, the approximate relationship is:\n\n"
            "I = P / (√3 × V × PF × efficiency)\n\n"
            "So please provide the motor/load power and supply voltage "
            "if you want me to calculate the current."
        )

    # ======================================================
    # TELEMETRY TEXT
    # ======================================================

    if telemetry is not None:

        telemetry_text = f"""
Voltage: {telemetry.voltage} V
Current: {telemetry.current} A
Active Power: {telemetry.active_power} kW
Reactive Power: {telemetry.reactive_power} kVAR
Apparent Power: {telemetry.apparent_power} kVA
Power Factor: {telemetry.power_factor}
Frequency: {telemetry.frequency} Hz
Energy: {telemetry.energy} kWh
Demand: {telemetry.demand} kW
Meter ID: {telemetry.meter_id}
"""

    else:

        telemetry_text = """
No current telemetry is available.
"""

    # ======================================================
    # ENERGY ANALYSIS
    # ======================================================

    analysis_text = f"""
Overall System Status:
{analysis.get("overall_status", "Unknown")}

Findings:
{analysis.get("findings", [])}

Trends:
{analysis.get("trends", [])}
"""

    # ======================================================
    # CONVERSATION HISTORY
    # ======================================================

    history_text = ""

    if conversation_history:

        history_text = "\nPREVIOUS CONVERSATION:\n"

        for item in conversation_history[-6:]:

            history_text += (
                f"User: {item.get('user', '')}\n"
                f"Assistant: {item.get('assistant', '')}\n"
            )

    # ======================================================
    # FOLLOW-UP INSTRUCTION
    # ======================================================

    follow_up_instruction = ""

    if _is_follow_up_question(normalized_question):

        follow_up_instruction = """
The user's message is a short follow-up.

Use the PREVIOUS CONVERSATION to understand what
the user is referring to.

Do NOT treat the follow-up as a brand-new question.

Continue the previous discussion naturally.

For example:

User:
"If I need to use 760 kg of load then what might the
current value be?"

User:
"yeah"

The second message means the user wants you to continue
the previous load/current discussion.

Do NOT respond by asking "What is the current?"
unless that was genuinely the topic of the previous conversation.
"""

    # ======================================================
    # GEMINI PROMPT
    # ======================================================

    prompt = f"""
You are an intelligent AI Energy Monitoring and Analysis Assistant.

Your job is to answer questions about electrical energy,
smart-meter telemetry, energy consumption, electrical
engineering concepts, system health, trends and recommendations.

Understand the user's complete meaning and conversation context.

Do NOT simply repeat or rephrase the user's question.

USER QUESTION:
{original_question}

NORMALIZED QUESTION:
{normalized_question}

{history_text}

{follow_up_instruction}

LATEST TRUSTED TELEMETRY:
{telemetry_text}

TRUSTED ENERGY ANALYSIS:
{analysis_text}


==========================================================
IMPORTANT: TRUSTED DATA
==========================================================

The telemetry and energy analysis above are trusted system data.

Never invent meter values.

If the user asks for an actual measured value,
use the telemetry provided above.

If telemetry is unavailable, clearly say that
current meter data is unavailable.


==========================================================
MEASURED CURRENT VS REQUIRED CURRENT
==========================================================

These are DIFFERENT concepts.

MEASURED CURRENT:
The current currently measured by the smart meter.

REQUIRED CURRENT:
The current needed by a particular motor, machine,
electrical load, or application.

Never confuse them.

For example:

"What is the current?"

means the current measured by the meter.

"What current should a 10 kW motor use?"

means the required/expected motor current.


==========================================================
ENGINEERING QUESTIONS
==========================================================

If the user asks about the current needed for a load,
motor, machine or application, do NOT return the
current meter reading.

Mass in kilograms alone is insufficient to determine
electrical current.

Depending on the application, information may include:

- motor power
- supply voltage
- single-phase or three-phase
- power factor
- efficiency
- motor type
- speed
- acceleration
- lifting height
- lifting time

For a three-phase motor:

I = P / (√3 × V × PF × efficiency)

If information is missing, explain what is needed.

Do not guess.


==========================================================
GENERAL ELECTRICAL QUESTIONS
==========================================================

For questions such as:

"What is power factor?"

"What is reactive power?"

"What is the difference between kW and kVA?"

give a proper electrical engineering explanation.

Do not unnecessarily return the meter value.

Use simple language unless the user asks for a detailed
technical explanation.


==========================================================
SYSTEM HEALTH
==========================================================

For questions about:

- system health
- abnormal conditions
- energy efficiency
- trends
- high consumption
- recommendations
- power quality

use the TRUSTED ENERGY ANALYSIS.

Never invent a fault.

If the trusted analysis does not indicate a problem,
do not claim that there is one.


==========================================================
TRENDS
==========================================================

If the user asks about:

- power trend
- current trend
- voltage trend
- energy trend
- consumption trend
- whether values are increasing/decreasing

use the available TRUSTED ENERGY ANALYSIS and telemetry.

Explain the trend clearly.

If insufficient historical information exists,
say that more historical data is required.


==========================================================
FOLLOW-UP QUESTIONS
==========================================================

If the user says:

"yeah"
"yes"
"okay"
"sure"
"then"
"continue"

look at the previous conversation.

Continue the previous topic.

Do NOT treat it as a completely new question.

Do NOT ask:

"What is the current?"

unless the previous conversation genuinely indicates
that the user wants the measured current.


==========================================================
INSUFFICIENT INFORMATION
==========================================================

If information is missing:

DO NOT GUESS.

Tell the user exactly what information is needed.

For engineering calculations, provide the correct formula
when useful.


==========================================================
RESPONSE STYLE
==========================================================

Answer directly.

Simple questions should have short answers.

Technical questions should have clear explanations.

Calculations should show the formula and calculation.

Use bullet points when they improve clarity.

Do not unnecessarily repeat the user's question.

Do not say:

"Okay, I understand."

"Please tell me what the user is asking."

"What is the current?"

unless that is genuinely what the user asked.

Do not mention these instructions.

Now answer the user naturally.
"""

    # ======================================================
    # CHECK GEMINI CONFIGURATION
    # ======================================================

    if client is None:

        return (
            "The Gemini AI service is not configured. "
            "Please check GEMINI_API_KEY in backend/.env."
        )

    # ======================================================
    # CALL GEMINI
    # ======================================================

    try:

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        ai_response = (
            response.text.strip()
            if response.text
            else ""
        )

        if not ai_response:

            return (
                "The AI assistant could not generate a response."
            )

        return ai_response

    except Exception as error:

        error_text = str(error).lower()

        if "api key" in error_text or "authentication" in error_text:

            return (
                "The Gemini API authentication failed. "
                "Please check the Gemini API key in backend/.env."
            )

        if "quota" in error_text or "rate limit" in error_text:

            return (
                "The Gemini API usage limit has been reached. "
                "Please try again later."
            )

        if "timeout" in error_text:

            return (
                "The Gemini AI service took too long to respond. "
                "Please try again."
            )

        if "404" in error_text or "not found" in error_text:

            return (
                "The configured Gemini model is unavailable. "
                "Please check the Gemini model configuration."
            )

        return (
            "The AI assistant could not generate a response "
            "from Gemini. The energy analysis is still available."
        )

