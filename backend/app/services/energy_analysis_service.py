
from typing import Dict, Any, List


def analyze_energy(
    telemetry,
    historical_readings: List[Any] | None = None
) -> Dict[str, Any]:
    """
    Analyze current electrical telemetry and recent
    historical readings to detect abnormal conditions
    and basic energy consumption trends.
    """

    findings = []
    trends = []

    # --------------------------------------------------
    # 1. VOLTAGE ANALYSIS
    # --------------------------------------------------

    if telemetry.voltage < 380:
        findings.append({
            "parameter": "Voltage",
            "status": "Low",
            "message": (
                f"Voltage is low at {telemetry.voltage} V."
            )
        })

    elif telemetry.voltage > 440:
        findings.append({
            "parameter": "Voltage",
            "status": "High",
            "message": (
                f"Voltage is high at {telemetry.voltage} V."
            )
        })

    else:
        findings.append({
            "parameter": "Voltage",
            "status": "Normal",
            "message": (
                f"Voltage is normal at {telemetry.voltage} V."
            )
        })

    # --------------------------------------------------
    # 2. POWER FACTOR ANALYSIS
    # --------------------------------------------------

    if telemetry.power_factor < 0.90:
        findings.append({
            "parameter": "Power Factor",
            "status": "Poor",
            "message": (
                f"Power factor is low at "
                f"{telemetry.power_factor}. "
                "This may indicate inefficient power usage."
            )
        })

    else:
        findings.append({
            "parameter": "Power Factor",
            "status": "Good",
            "message": (
                f"Power factor is good at "
                f"{telemetry.power_factor}."
            )
        })

    # --------------------------------------------------
    # 3. FREQUENCY ANALYSIS
    # --------------------------------------------------

    if telemetry.frequency < 49:
        findings.append({
            "parameter": "Frequency",
            "status": "Low",
            "message": (
                f"Frequency is low at "
                f"{telemetry.frequency} Hz."
            )
        })

    elif telemetry.frequency > 51:
        findings.append({
            "parameter": "Frequency",
            "status": "High",
            "message": (
                f"Frequency is high at "
                f"{telemetry.frequency} Hz."
            )
        })

    else:
        findings.append({
            "parameter": "Frequency",
            "status": "Normal",
            "message": (
                f"Frequency is normal at "
                f"{telemetry.frequency} Hz."
            )
        })

    # --------------------------------------------------
    # 4. ACTIVE POWER ANALYSIS
    # --------------------------------------------------

    if telemetry.active_power > 100:
        findings.append({
            "parameter": "Active Power",
            "status": "High",
            "message": (
                f"Active power is relatively high at "
                f"{telemetry.active_power} kW."
            )
        })

    else:
        findings.append({
            "parameter": "Active Power",
            "status": "Normal",
            "message": (
                f"Active power is "
                f"{telemetry.active_power} kW."
            )
        })

    # --------------------------------------------------
    # 5. HISTORICAL POWER TREND ANALYSIS
    # --------------------------------------------------

    if historical_readings and len(historical_readings) >= 3:

        # Extract active power values
        power_values = [
            float(reading.active_power)
            for reading in historical_readings
        ]

        # Current and previous readings
        current_power = power_values[0]
        previous_power = power_values[1]

        # Calculate change percentage
        if previous_power != 0:
            power_change = (
                (current_power - previous_power)
                / abs(previous_power)
            ) * 100
        else:
            power_change = 0

        # Detect sudden increase
        if power_change >= 20:
            trends.append({
                "parameter": "Active Power Trend",
                "status": "Increasing",
                "message": (
                    f"Active power increased by "
                    f"{power_change:.1f}% compared with "
                    "the previous reading."
                )
            })

        # Detect sudden decrease
        elif power_change <= -20:
            trends.append({
                "parameter": "Active Power Trend",
                "status": "Decreasing",
                "message": (
                    f"Active power decreased by "
                    f"{abs(power_change):.1f}% compared with "
                    "the previous reading."
                )
            })

        # Stable power
        else:
            trends.append({
                "parameter": "Active Power Trend",
                "status": "Stable",
                "message": (
                    "Active power is relatively stable "
                    "compared with the previous reading."
                )
            })

        # --------------------------------------------------
        # Recent average power
        # --------------------------------------------------

        average_power = (
            sum(power_values) / len(power_values)
        )

        trends.append({
            "parameter": "Average Active Power",
            "status": "Information",
            "message": (
                f"Average active power across the recent "
                f"{len(power_values)} readings is "
                f"{average_power:.2f} kW."
            )
        })

    else:
        trends.append({
            "parameter": "Active Power Trend",
            "status": "Insufficient Data",
            "message": (
                "Not enough historical readings are available "
                "to determine a reliable power trend."
            )
        })

    # --------------------------------------------------
    # 6. OVERALL HEALTH
    # --------------------------------------------------

    abnormal_findings = [
        finding
        for finding in findings
        if finding["status"] in [
            "Low",
            "High",
            "Poor"
        ]
    ]

    abnormal_trends = [
        trend
        for trend in trends
        if trend["status"] in [
            "Increasing",
            "Decreasing"
        ]
    ]

    if abnormal_findings or abnormal_trends:
        overall_status = "Attention Required"
    else:
        overall_status = "Healthy"

    # --------------------------------------------------
    # 7. FINAL ANALYSIS RESULT
    # --------------------------------------------------

    return {
        "overall_status": overall_status,
        "findings": findings,
        "trends": trends
    }

