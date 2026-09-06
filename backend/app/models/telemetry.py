"""
SQLAlchemy database model for electrical telemetry readings.
"""

from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class TelemetryReadingModel(Base):
    """
    Database model representing one electrical meter reading.
    """

    __tablename__ = "telemetry_readings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    voltage: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    current: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    active_power: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    reactive_power: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    apparent_power: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    power_factor: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    frequency: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    energy: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    demand: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    meter_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )