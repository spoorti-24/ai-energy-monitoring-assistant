# AI Energy Monitoring and Analysis Assistant

An industrial IoT platform designed to collect, process, and analyze electrical telemetry metrics from Schneider smart meters (simulated using a decoupled `MockMeterConnector` in initial phases) with AI agent capabilities and a modern React dashboard interface.

---

## 🏗️ Architecture Stack

- **Backend**: Python 3.10+, FastAPI, Pydantic, SQLAlchemy
- **Database**: PostgreSQL
- **Hardware Integration Layer**: Abstract `MeterConnector` interface (`MockMeterConnector` for stage 1)
- **Frontend**: React + TypeScript (Vite)
- **AI Integration**: Designed for tool calling & automated energy telemetry analytics (stage 2)

---

## 📁 Repository Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/          # Route controllers (GET /health)
│   │   ├── config/       # Environment & app settings
│   │   ├── connectors/   # Hardware layer (base.py & mock_meter.py)
│   │   ├── database/     # DB session & engine configuration
│   │   ├── models/       # SQLAlchemy database models
│   │   ├── schemas/      # Pydantic validation schemas
│   │   ├── services/     # Business logic layer
│   │   └── main.py       # FastAPI application entry point
│   ├── .env.example      # Environment variables template
│   └── requirements.txt  # Dependencies list
├── frontend/             # React + TypeScript Web Application
├── tests/                # Automated pytest suite
└── docs/                 # System documentation
```

---

## 🚀 Quickstart Guide

### 1. Backend Setup

```powershell
# Navigate to workspace root
cd "c:\Users\Spoorti S Rayannavar\Desktop\Incident_Intelligent_Platform\zf ai chatbot"

# Create Python virtual environment
python -m venv .venv

# Activate virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Install requirements
pip install -r backend/requirements.txt

# Create .env from template
cp backend/.env.example backend/.env

# Run FastAPI server
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Verify API Health

- **Health Check Endpoint**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health) -> Returns `{"status": "ok"}`
- **Interactive Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 3. Run Automated Tests

```powershell
# Make sure virtual environment is active and run pytest
pytest tests/
```
