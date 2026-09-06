"""
Pydantic schemas package for request and response validation.
"""
from app.schemas.telemetry import TelemetryReading, MeterStatusResponse

__all__ = ["TelemetryReading", "MeterStatusResponse"]
