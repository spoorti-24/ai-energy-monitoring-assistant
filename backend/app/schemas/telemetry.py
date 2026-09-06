from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class TelemetryReading(BaseModel):
    """
    Pydantic schema for industrial smart meter electrical telemetry.
    Validates data types, units, and realistic physical operating limits.
    """
    timestamp: str = Field(
        ...,
        description="ISO 8601 UTC timestamp string of the reading"
    )
    voltage: float = Field(
        ...,
        ge=300.0,
        le=500.0,
        description="Line-to-line 3-phase AC voltage in Volts (V)"
    )
    current: float = Field(
        ...,
        ge=0.0,
        le=500.0,
        description="3-phase line current in Amperes (A)"
    )
    active_power: float = Field(
        ...,
        ge=0.0,
        description="Active / Real power delivered in kilowatts (kW)"
    )
    reactive_power: float = Field(
        ...,
        ge=0.0,
        description="Reactive power in kilovar (kVAR)"
    )
    apparent_power: float = Field(
        ...,
        ge=0.0,
        description="Apparent power in kilovolt-amperes (kVA)"
    )
    power_factor: float = Field(
        ...,
        ge=0.80,
        le=0.99,
        description="Power factor (unitless, ratio between 0.80 and 0.99)"
    )
    frequency: float = Field(
        ...,
        ge=45.0,
        le=55.0,
        description="Electrical grid frequency in Hertz (Hz)"
    )
    energy: float = Field(
        ...,
        ge=0.0,
        description="Cumulative active energy consumed in kilowatt-hours (kWh)"
    )
    demand: float = Field(
        ...,
        ge=0.0,
        description="Active power demand in kilowatts (kW)"
    )
    meter_id: Optional[str] = Field(
        default="MOCK-SCHNEIDER-001",
        description="Unique identifier of the smart meter device"
    )

    @field_validator("timestamp")
    @classmethod
    def validate_iso_timestamp(cls, value: str) -> str:
        """Verify timestamp can be parsed as a valid ISO 8601 string."""
        try:
            datetime.fromisoformat(value)
        except ValueError:
            raise ValueError(f"Invalid ISO 8601 timestamp format: {value}")
        return value


class MeterStatusResponse(BaseModel):
    """
    Pydantic schema for smart meter connector connection status response.
    """
    connected: bool = Field(
        ...,
        description="Indicates if the backend is actively connected to the meter connector"
    )
    meter_id: str = Field(
        ...,
        description="Identifier of the smart meter hardware or software bridge"
    )
    connector_type: str = Field(
        ...,
        description="Type of connector active in backend (e.g. 'mock' or 'schneider')"
    )
