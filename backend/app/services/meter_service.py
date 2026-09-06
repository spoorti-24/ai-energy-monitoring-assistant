from typing import Optional

from app.config import settings
from app.connectors.base import MeterConnector
from app.connectors.mock_meter import MockMeterConnector
from app.schemas.telemetry import TelemetryReading, MeterStatusResponse
from app.repositories.telemetry_repository import save_telemetry


class MeterService:
    """
    Service layer orchestrating energy meter operations.

    Decouples FastAPI API route handlers from hardware connector instances.
    Selects connector based on environment settings and validates output schemas.
    """

    def __init__(
        self,
        connector: Optional[MeterConnector] = None,
        connector_type: Optional[str] = None
    ):
        self.connector_type = (
            connector_type or settings.METER_CONNECTOR_TYPE.lower()
        )

        if connector is not None:
            self.connector = connector
        else:
            self.connector = self._create_connector(self.connector_type)

    def _create_connector(self, connector_type: str) -> MeterConnector:
        """Connector Factory: Instantiates appropriate MeterConnector implementation."""

        if connector_type == "mock":
            return MockMeterConnector()

        # Future extension:
        # elif connector_type == "schneider":
        #     return SchneiderMeterConnector()

        else:
            # Fallback to MockMeterConnector for safety
            return MockMeterConnector()

    def get_current_telemetry(self, db) -> TelemetryReading:
        """
        Obtains current meter telemetry data,
        validates it, and saves it to PostgreSQL.
        """

        if not self.connector.is_connected():
            self.connector.connect()

        # Get raw telemetry from meter
        raw_telemetry = self.connector.read_telemetry()

        # Validate telemetry using Pydantic
        telemetry = TelemetryReading(**raw_telemetry)

        # Save validated telemetry to PostgreSQL
        save_telemetry(db, telemetry)

        return telemetry

    def get_meter_status(self) -> MeterStatusResponse:
        """
        Obtains current connector connection status.
        """

        if not self.connector.is_connected():
            self.connector.connect()

        return MeterStatusResponse(
            connected=self.connector.is_connected(),
            meter_id=getattr(
                self.connector,
                "meter_id",
                "UNKNOWN-METER"
            ),
            connector_type=self.connector_type
        )


# Singleton instance of MeterService for application lifetime
_meter_service_instance: Optional[MeterService] = None


def get_meter_service() -> MeterService:
    """FastAPI Dependency Provider returning initialized MeterService instance."""

    global _meter_service_instance

    if _meter_service_instance is None:
        _meter_service_instance = MeterService()

    return _meter_service_instance