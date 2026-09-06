from abc import ABC, abstractmethod
from typing import Dict, Any


class MeterConnector(ABC):
    """
    Abstract Base Class for Energy Meter Connectors.
    
    All hardware connectors (Mock, Schneider, Modbus, MQTT, REST, etc.)
    must inherit from this interface and implement its abstract methods.
    
    This ensures the backend application remains completely independent of the
    underlying hardware meter vendor and connection protocol.
    """

    @abstractmethod
    def connect(self) -> bool:
        """
        Establishes connection to the energy meter or software bridge.
        Returns True if successful, False otherwise.
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """
        Gracefully terminates the connection to the meter.
        """
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """
        Checks current connection state to the meter.
        """
        pass

    @abstractmethod
    def read_telemetry(self) -> Dict[str, Any]:
        """
        Reads latest electrical telemetry measurements from the smart meter.
        
        Expected fields in return dictionary:
        - timestamp (str): ISO 8601 string timestamp
        - voltage (float): Line-to-line 3-phase voltage in V
        - current (float): 3-phase line current in A
        - active_power (float): Active/Real power in kW
        - reactive_power (float): Reactive power in kVAR
        - apparent_power (float): Apparent power in kVA
        - power_factor (float): Power factor (unitless, 0.80 to 0.99)
        - frequency (float): Grid frequency in Hz
        - energy (float): Cumulative active energy in kWh
        - demand (float): Peak active power demand in kW
        - meter_id (str): Meter hardware identifier
        """
        pass

