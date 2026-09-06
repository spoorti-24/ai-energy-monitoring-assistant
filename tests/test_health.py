from fastapi.testclient import TestClient
from app.main import app
from app.connectors.mock_meter import MockMeterConnector

client = TestClient(app)


def test_get_health():
    """
    Test GET /health returns HTTP status 200 and JSON {"status": "ok"}.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_mock_meter_connector_health():
    """
    Test MockMeterConnector connection state and telemetry payload.
    """
    connector = MockMeterConnector(meter_id="TEST-METER-01")
    assert connector.connect() is True
    assert connector.is_connected() is True

    telemetry = connector.read_telemetry()
    assert telemetry["meter_id"] == "TEST-METER-01"
    assert 380.0 <= telemetry["voltage"] <= 440.0
    assert 10.0 <= telemetry["current"] <= 100.0
    assert "timestamp" in telemetry

    connector.disconnect()
    assert connector.is_connected() is False
