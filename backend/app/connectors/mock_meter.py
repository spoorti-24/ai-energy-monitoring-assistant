import math
import random
import time
from datetime import datetime, timezone
from typing import Dict, Any

from app.connectors.base import MeterConnector


class MockMeterConnector(MeterConnector):
    """
    Mock implementation of MeterConnector for Phase 2.
    
    Simulates a realistic 3-phase industrial smart meter, generating electrical
    telemetry with proper physical relationships (Apparent Power S, Active Power P,
    Reactive Power Q, Power Factor PF, Voltage V, Current I, Frequency Hz,
    Cumulative Energy kWh, and Demand kW).
    """

    def __init__(self, meter_id: str = "MOCK-SCHNEIDER-001"):
        self.meter_id = meter_id
        self._connected: bool = False
        
        # Base state for realistic operating conditions around nominal values
        self._base_voltage: float = 415.0       # 3-Phase line voltage (~415 V)
        self._base_current: float = 35.0        # 3-Phase line current (~35 A)
        self._accumulated_energy: float = 12450.55  # Cumulative energy counter (kWh)
        self._peak_demand: float = 25.80        # Peak active power demand (kW)
        self._last_read_time: float = time.time()

    def connect(self) -> bool:
        """Establishes connection to simulated meter."""
        self._connected = True
        self._last_read_time = time.time()
        return True

    def disconnect(self) -> None:
        """Terminates connection to simulated meter."""
        self._connected = False

    def is_connected(self) -> bool:
        """Checks connection status."""
        return self._connected

    def read_telemetry(self) -> Dict[str, Any]:
        """
        Generates realistic 3-phase industrial smart meter telemetry payload.
        
        Returns dictionary containing all 10 required telemetry fields:
        1. timestamp (ISO 8601 UTC string)
        2. voltage (V)
        3. current (A)
        4. active_power (kW)
        5. reactive_power (kVAR)
        6. apparent_power (kVA)
        7. power_factor (unitless, 0.80 - 0.99)
        8. frequency (Hz)
        9. energy (kWh, cumulative)
        10. demand (kW)
        """
        if not self._connected:
            self.connect()

        now_time = time.time()
        dt = max(now_time - self._last_read_time, 1.0)  # Elapsed time in seconds
        self._last_read_time = now_time

        # Generate realistic variations around operating parameters
        # Voltage: line-to-line 3-phase ~415 V (within 405 V - 425 V)
        voltage = round(self._base_voltage + random.uniform(-5.0, 5.0), 2)

        # Current: 3-phase line current ~35 A (within 20 A - 50 A)
        current = round(self._base_current + random.uniform(-8.0, 8.0), 2)

        # Power Factor: industrial inductive load between 0.80 and 0.99
        power_factor = round(random.uniform(0.85, 0.97), 2)

        # Frequency: nominal 50 Hz grid frequency (49.80 Hz - 50.20 Hz)
        frequency = round(50.0 + random.uniform(-0.15, 0.15), 2)

        # Three-phase Apparent Power S (kVA) = (sqrt(3) * V_line * I_line) / 1000
        apparent_power = round((math.sqrt(3) * voltage * current) / 1000.0, 2)

        # Active Power P (kW) = S * PF
        active_power = round(apparent_power * power_factor, 2)

        # Reactive Power Q (kVAR) = sqrt(S^2 - P^2)
        q_squared = max(0.0, apparent_power**2 - active_power**2)
        reactive_power = round(math.sqrt(q_squared), 2)

        # Energy increment in kWh = P (kW) * dt (hours)
        energy_increment = (active_power * dt) / 3600.0
        self._accumulated_energy += energy_increment
        energy = round(self._accumulated_energy, 2)

        # Peak / Rolling Demand in kW
        if active_power > self._peak_demand:
            self._peak_demand = active_power
        demand = round(self._peak_demand, 2)

        timestamp_str = datetime.now(timezone.utc).isoformat()

        return {
            "timestamp": timestamp_str,
            "voltage": voltage,
            "current": current,
            "active_power": active_power,
            "reactive_power": reactive_power,
            "apparent_power": apparent_power,
            "power_factor": power_factor,
            "frequency": frequency,
            "energy": energy,
            "demand": demand,
            "meter_id": self.meter_id
        }
