# Architecture Documentation

## Overview

The **AI Energy Monitoring and Analysis Assistant** is built to monitor industrial energy consumption metrics, identify power anomalies, and support AI-driven telemetry analytics.

```
+-------------------------------------------------------------+
|                      Data Source                            |
|  [ MockMeterConnector ] ---> (Future: Schneider Meter API)  |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                  Meter Connector Layer                      |
|  Abstract Base Class (base.py) defines standard interface   |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                     FastAPI Backend                         |
|   Routers (api/) <--> Business Services <--> Schemas/Models  |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                   PostgreSQL Database                       |
|          SQLAlchemy ORM + Connection Pooling                |
+------------------------------+------------------------------+
                               | (Backend Function Tools)
                               v
+-------------------------------------------------------------+
|                       AI Agent                              |
|           Analyzes trends, anomalies & telemetry            |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                 React Web Application                       |
|             Dashboard + AI Chat Interface                   |
+-------------------------------------------------------------+
```

## Meter Connector Abstract Interface

The system utilizes Python's Abstract Base Class pattern (`abc.ABC`) to ensure zero coupling between application services and specific meter hardware/software implementations.

```python
class MeterConnector(ABC):
    @abstractmethod
    def connect(self) -> bool: pass
    
    @abstractmethod
    def disconnect(self) -> None: pass
    
    @abstractmethod
    def is_connected(self) -> bool: pass
    
    @abstractmethod
    def read_telemetry(self) -> Dict[str, Any]: pass
```

### Swapping from Mock to Schneider

When the Schneider meter specification is delivered:
1. Implement `SchneiderMeterConnector` inheriting from `MeterConnector` in `backend/app/connectors/schneider_meter.py`.
2. Update `METER_CONNECTOR_TYPE="schneider"` in `.env`.
3. No modifications are needed in FastAPI routers, SQLAlchemy models, or AI functions.
