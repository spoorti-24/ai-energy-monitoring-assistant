# AI Energy Monitoring and Analysis Assistant

An industrial IoT platform designed to collect, store, process, and analyze electrical telemetry data from smart meters, with AI-powered energy analysis and a modern React dashboard.

The current development version uses a decoupled `MockMeterConnector` to simulate Schneider smart-meter data. The connector layer is designed so that the mock source can later be replaced with the actual Schneider REST API when the required API details are provided.

---

## 🏗️ Architecture

```text
Mock / Schneider Smart Meter
          ↓
   Meter Connector Layer
          ↓
      FastAPI Backend
          ↓
      PostgreSQL DB
          ↓
   Energy Analysis Service
          ↓
      Gemini AI Service
          ↓
    React Web Dashboard
```

---

## 🛠️ Technology Stack

* **Backend:** Python 3.10+, FastAPI, Pydantic, SQLAlchemy
* **Database:** PostgreSQL
* **Hardware Integration:** Abstract `MeterConnector` interface
* **Current Meter Source:** `MockMeterConnector`
* **Frontend:** React + TypeScript + Vite
* **AI:** Google Gemini API
* **Testing:** pytest

---

## 📁 Repository Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/              # API route controllers
│   │   ├── config/           # Application configuration
│   │   ├── connectors/       # Meter connector layer
│   │   │   ├── base.py
│   │   │   └── mock_meter.py
│   │   ├── database/         # PostgreSQL database configuration
│   │   ├── models/           # SQLAlchemy models
│   │   ├── repositories/     # Database access layer
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business and AI logic
│   │   └── main.py           # FastAPI entry point
│   ├── .env.example          # Environment variable template
│   └── requirements.txt      # Python dependencies
│
├── frontend/                 # React + TypeScript application
│
├── tests/                    # Automated pytest tests
│
├── docs/                     # System documentation
│
├── package.json
├── package-lock.json
├── pytest.ini
└── README.md
```

---

# 🚀 Running the Project on a New Computer

## Prerequisites

Install the following before running the project:

* Python 3.10 or newer
* Node.js and npm
* PostgreSQL
* Git

The current version uses a **mock meter**, so Schneider hardware is **not required** for development.

---

# 1. Clone the Repository

Open PowerShell or a terminal:

```powershell
git clone https://github.com/spoorti-24/ai-energy-monitoring-assistant.git
cd ai-energy-monitoring-assistant
```

---

# 2. Backend Setup

Create a Python virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the backend dependencies:

```powershell
pip install -r backend/requirements.txt
```

---

# 3. PostgreSQL Database Setup

Make sure PostgreSQL is installed and running.

Create a database named:

```text
energy_monitoring
```

The database credentials are configured through the backend `.env` file.

---

# 4. Configure Backend Environment Variables

Copy the example environment file:

```powershell
Copy-Item backend\.env.example backend\.env
```

Open:

```text
backend/.env
```

Configure the database settings according to your local PostgreSQL installation.

Example:

```env
DB_HOST="localhost"
DB_PORT=5432
DB_NAME="energy_monitoring"
DB_USER="postgres"
DB_PASSWORD="YOUR_POSTGRES_PASSWORD"
```

For the current mock-meter setup:

```env
METER_CONNECTOR_TYPE="mock"
```

---

# 5. Configure Gemini AI

The AI assistant uses the Google Gemini API.

Create your own Gemini API key and add it to your local:

```text
backend/.env
```

Example:

```env
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

**Never commit or share your `.env` file or API key.**

The repository only contains:

```text
backend/.env.example
```

---

# 6. Start the Backend

From the project root:

```powershell
set PYTHONPATH=backend
.\.venv\Scripts\uvicorn.exe app.main:app --reload --host 127.0.0.1 --port 8000
```

The backend will run at:

```text
http://127.0.0.1:8000
```

Keep this terminal running.

---

# 7. Verify the Backend

Open:

```text
http://127.0.0.1:8000/health
```

You should receive a successful health response.

Swagger API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

# 8. Frontend Setup

Open a **second terminal**.

Navigate to the frontend:

```powershell
cd frontend
```

Install the frontend dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

Vite will display the local frontend URL in the terminal, normally:

```text
http://localhost:5173
```

Open that URL in your browser.

---

# 9. Running Both Services

You need **two terminals** running at the same time.

### Terminal 1 — Backend

```powershell
cd "ai-energy-monitoring-assistant"
.\.venv\Scripts\Activate.ps1
set PYTHONPATH=backend
.\.venv\Scripts\uvicorn.exe app.main:app --reload --host 127.0.0.1 --port 8000
```

### Terminal 2 — Frontend

```powershell
cd "ai-energy-monitoring-assistant\frontend"
npm run dev
```

Then open the frontend URL shown by Vite.

---

# 🧪 Running Automated Tests

Activate the Python virtual environment and run:

```powershell
pytest tests/
```

The test suite covers the backend health endpoint, mock meter functionality, and meter API behavior.

---

# ⚡ Current Features

The current working version includes:

* Real-time electrical telemetry
* Mock smart-meter data source
* Meter connection/status information
* PostgreSQL telemetry storage
* Historical power data
* Power consumption graph
* Electrical measurements including:

  * Voltage
  * Current
  * Active Power
  * Reactive Power
  * Apparent Power
  * Power Factor
  * Frequency
  * Energy
  * Demand
* Energy trend analysis
* AI Energy Assistant
* Gemini-powered conversational responses
* Conversation context for follow-up questions
* Electrical engineering explanations
* Protection against unsupported calculations and invented meter values

---

# 🔌 Schneider Meter Integration

The project uses a connector abstraction so the current mock source can later be replaced by the actual Schneider integration.

Current:

```text
MockMeterConnector
       ↓
MeterService
       ↓
FastAPI
```

Planned:

```text
Schneider REST API
       ↓
Schneider Meter Connector
       ↓
MeterService
       ↓
FastAPI
```

The actual Schneider integration will be implemented once the required API endpoint, authentication method, telemetry format, and meter information are available.

---

# 🔐 Security

Do not commit:

```text
.env
*.env
```

API keys, passwords, and other secrets must remain local.

The repository contains `.env.example` only as a configuration template.

---

# 👥 Team Development

This repository contains the current working baseline of the AI Energy Monitoring and Analysis Assistant.

Before making major changes:

```powershell
git pull origin main
```

After making and testing changes:

```powershell
git add .
git commit -m "Describe your change"
git push
```

For larger features, create a separate Git branch before development.

---

## 📌 Project Status

**Current stage:** Working development prototype

**Meter source:** Mock meter

**AI:** Google Gemini

**Database:** PostgreSQL

**Frontend:** React + TypeScript

**Next major integration:** Actual Schneider smart-meter REST API
