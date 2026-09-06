import math
import time
from datetime import datetime

from app.connectors.mock_meter import MockMeterConnector
from app.schemas.telemetry import TelemetryReading


def test_telemetry_generation():
    """1. Test telemetry generation: connector initializes and reads data cleanly."""
    connector = MockMeterConnector(meter_id="TEST-MOCK-001")
    assert connector.connect() is True
    assert connector.is_connected() is True

    telemetry = connector.read_telemetry()
    assert isinstance(telemetry, dict)
    assert telemetry["meter_id"] == "TEST-MOCK-001"

    connector.disconnect()
    assert connector.is_connected() is False


def test_required_fields():
    """2. Test required fields: all 10 standard telemetry metrics are present."""
    connector = MockMeterConnector()
    telemetry = connector.read_telemetry()

    required_fields = [
        "timestamp",
        "voltage",
        "current",
        "active_power",
        "reactive_power",
        "apparent_power",
        "power_factor",
        "frequency",
        "energy",
        "demand"
    ]

    for field in required_fields:
        assert field in telemetry, f"Missing required telemetry field: {field}"

    # Also validate against Pydantic schema
    reading_schema = TelemetryReading(**telemetry)
    assert reading_schema.meter_id == "MOCK-SCHNEIDER-001"


def test_valid_ranges():
    """3. Test valid ranges: 3-phase values fall within realistic operating limits."""
    connector = MockMeterConnector()
    telemetry = connector.read_telemetry()

    assert 380.0 <= telemetry["voltage"] <= 440.0, f"Voltage out of range: {telemetry['voltage']}"
    assert 10.0 <= telemetry["current"] <= 100.0, f"Current out of range: {telemetry['current']}"
    assert 48.0 <= telemetry["frequency"] <= 52.0, f"Frequency out of range: {telemetry['frequency']}"
    assert telemetry["active_power"] > 0.0
    assert telemetry["apparent_power"] > 0.0
    assert telemetry["reactive_power"] >= 0.0
    assert telemetry["demand"] > 0.0


def test_power_factor_validity():
    """4. Test power factor validity: must be between 0.80 and 0.99."""
    connector = MockMeterConnector()

    for _ in range(10):
        telemetry = connector.read_telemetry()
        pf = telemetry["power_factor"]
        assert 0.80 <= pf <= 0.99, f"Power factor {pf} out of [0.80, 0.99] bounds"


def test_timestamp_validity():
    """5. Test timestamp validity: must be a valid ISO 8601 string."""
    connector = MockMeterConnector()
    telemetry = connector.read_telemetry()

    timestamp_str = telemetry["timestamp"]
    parsed_dt = datetime.fromisoformat(timestamp_str)
    assert isinstance(parsed_dt, datetime)


def test_repeated_readings():
    """6. Test repeated readings: values fluctuate naturally across calls."""
    connector = MockMeterConnector()
    readings = [connector.read_telemetry() for _ in range(5)]

    voltages = [r["voltage"] for r in readings]
    currents = [r["current"] for r in readings]

    # Verify repeated readings are not static identical hardcoded constants
    assert len(set(voltages)) > 1, "Voltages should show realistic natural variation"
    assert len(set(currents)) > 1, "Currents should show realistic natural variation"


def test_energy_is_cumulative_non_decreasing():
    """7. Test energy is cumulative/non-decreasing: energy_2 >= energy_1."""
    connector = MockMeterConnector()

    readings = []
    for _ in range(5):
        readings.append(connector.read_telemetry())
        time.sleep(0.01)

    energies = [r["energy"] for r in readings]
    for i in range(len(energies) - 1):
        assert energies[i + 1] >= energies[i], (
            f"Energy decreased: {energies[i]} -> {energies[i + 1]}"
        )


def test_basic_electrical_consistency():
    """8. Test basic electrical consistency: S >= P, P ~ S*PF, S ~ sqrt(P^2 + Q^2)."""
    connector = MockMeterConnector()

    for _ in range(5):
        telemetry = connector.read_telemetry()

        s = telemetry["apparent_power"]
        p = telemetry["active_power"]
        q = telemetry["reactive_power"]
        pf = telemetry["power_factor"]

        # Apparent power must be >= active power
        assert s >= p, f"Apparent power ({s}) must be >= active power ({p})"

        # P ~ S * PF (allowing 0.05 rounding tolerance)
        expected_p = s * pf
        assert abs(p - expected_p) <= 0.05, (
            f"Active power {p} inconsistent with S={s} * PF={pf} ({expected_p})"
        )

        # S ~ sqrt(P^2 + Q^2) (allowing 0.1 rounding tolerance)
        calculated_s = math.sqrt(p**2 + q**2)
        assert abs(s - calculated_s) <= 0.1, (
            f"Apparent power {s} inconsistent with sqrt(P^2 + Q^2)={calculated_s}"
        )
