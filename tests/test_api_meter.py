from fastapi.testclient import TestClient
from app.main import app
from app.schemas.telemetry import TelemetryReading, MeterStatusResponse

client = TestClient(app)


def test_health_endpoint_still_works():
    """1. Test GET /health still returns HTTP 200 and {"status": "ok"}."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_meter_current_http_200():
    """2. Test GET /api/meter/current returns HTTP 200."""
    response = client.get("/api/meter/current")
    assert response.status_code == 200


def test_get_meter_current_required_fields():
    """3. Test current telemetry response contains all required fields."""
    response = client.get("/api/meter/current")
    data = response.json()

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
        assert field in data, f"Field '{field}' missing from GET /api/meter/current response"


def test_get_meter_current_pydantic_validation():
    """4. Test returned telemetry satisfies Pydantic validation rules."""
    response = client.get("/api/meter/current")
    data = response.json()

    reading = TelemetryReading(**data)
    assert 380.0 <= reading.voltage <= 440.0
    assert 0.80 <= reading.power_factor <= 0.99
    assert reading.apparent_power >= reading.active_power


def test_get_meter_status_http_200():
    """5. Test GET /api/meter/status returns HTTP 200."""
    response = client.get("/api/meter/status")
    assert response.status_code == 200


def test_get_meter_status_response_body():
    """6. Test status correctly reports mock connector info."""
    response = client.get("/api/meter/status")
    data = response.json()

    status = MeterStatusResponse(**data)
    assert status.connected is True
    assert status.connector_type == "mock"
    assert status.meter_id == "MOCK-SCHNEIDER-001"
