import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import "./App.css";

interface Telemetry {
  timestamp: string;
  voltage: number;
  current: number;
  active_power: number;
  reactive_power: number;
  apparent_power: number;
  power_factor: number;
  frequency: number;
  energy: number;
  demand: number;
  meter_id: string;
}

interface MeterStatus {
  connected: boolean;
  meter_id: string;
  connector_type: string;
}

interface ChartReading {
  time: string;
  power: number;
}

interface ChatMessage {
  sender: "user" | "assistant";
  text: string;
}

interface AnalysisFinding {
  parameter: string;
  status: string;
  message: string;
}

interface AnalysisTrend {
  parameter: string;
  status: string;
  message: string;
}

interface EnergyAnalysis {
  overall_status: string;
  findings: AnalysisFinding[];
  trends: AnalysisTrend[];
  llm_response?: string;
}

function App() {
  const [telemetry, setTelemetry] =
    useState<Telemetry | null>(null);

  const [status, setStatus] =
    useState<MeterStatus | null>(null);

  const [error, setError] =
    useState<string>("");

  const [powerHistory, setPowerHistory] =
    useState<ChartReading[]>([]);

  const [chatOpen, setChatOpen] =
    useState<boolean>(false);

  const [message, setMessage] =
    useState<string>("");

  const [chatMessages, setChatMessages] =
    useState<ChatMessage[]>([]);

  const [isThinking, setIsThinking] =
    useState<boolean>(false);

  const API_URL =
    "http://127.0.0.1:8000";

  // --------------------------------------------------
  // CURRENT TELEMETRY
  // --------------------------------------------------

  const fetchCurrentData = async (): Promise<void> => {
    try {
      const response = await fetch(
        `${API_URL}/api/meter/current`
      );

      if (!response.ok) {
        throw new Error(
          "Current telemetry request failed"
        );
      }

      const data: Telemetry =
        await response.json();

      setTelemetry(data);
      setError("");
    } catch (error) {
      console.error(error);

      setError(
        "Unable to connect to backend"
      );
    }
  };

  // --------------------------------------------------
  // METER STATUS
  // --------------------------------------------------

  const fetchStatus = async (): Promise<void> => {
    try {
      const response = await fetch(
        `${API_URL}/api/meter/status`
      );

      if (!response.ok) {
        throw new Error(
          "Meter status request failed"
        );
      }

      const data: MeterStatus =
        await response.json();

      setStatus(data);
    } catch (error) {
      console.error(error);
    }
  };

  // --------------------------------------------------
  // HISTORY
  // --------------------------------------------------

  const fetchHistory = async (): Promise<void> => {
    try {
      const response = await fetch(
        `${API_URL}/api/meter/history`
      );

      if (!response.ok) {
        throw new Error(
          "History request failed"
        );
      }

      const history: Telemetry[] =
        await response.json();

      const chartData: ChartReading[] =
        history
          .slice()
          .reverse()
          .slice(-20)
          .map((reading) => ({
            time: new Date(
              reading.timestamp
            ).toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
              second: "2-digit",
            }),

            power: Number(
              reading.active_power
            ),
          }));

      setPowerHistory(chartData);
    } catch (error) {
      console.error(error);
    }
  };

  // --------------------------------------------------
  // FETCH ALL DASHBOARD DATA
  // --------------------------------------------------

  const fetchData = async (): Promise<void> => {
    await Promise.all([
      fetchCurrentData(),
      fetchStatus(),
      fetchHistory(),
    ]);
  };

  // --------------------------------------------------
  // AI CHAT
  // --------------------------------------------------

  const handleChat = async (): Promise<void> => {
    const userMessage =
      message.trim();

    if (userMessage === "") {
      return;
    }

    const userChat: ChatMessage = {
      sender: "user",
      text: userMessage,
    };

    setChatMessages((previous) => [
      ...previous,
      userChat,
    ]);

    setMessage("");
    setIsThinking(true);

    try {
      /*
       * Send the actual user question
       * to the FastAPI backend.
       *
       * Backend flow:
       *
       * PostgreSQL
       *      ↓
       * Energy Analysis
       *      ↓
       * Gemini AI
       *      ↓
       * AI Response
       */

      const analysisResponse = await fetch(
        `${API_URL}/api/meter/analysis?question=${encodeURIComponent(
          userMessage
        )}`
      );

      if (!analysisResponse.ok) {
        throw new Error(
          "Energy analysis request failed"
        );
      }

      const analysis: EnergyAnalysis =
        await analysisResponse.json();

      const aiResponse =
        analysis.llm_response ??
        "The AI assistant could not generate a response.";

      const assistantChat: ChatMessage = {
        sender: "assistant",
        text: aiResponse,
      };

      setChatMessages((previous) => [
        ...previous,
        assistantChat,
      ]);
    } catch (error) {
      console.error(
        "AI chat error:",
        error
      );

      const assistantChat: ChatMessage = {
        sender: "assistant",
        text:
          "I could not retrieve the AI response from the backend. Please make sure FastAPI is running and the Gemini API configuration is available.",
      };

      setChatMessages((previous) => [
        ...previous,
        assistantChat,
      ]);
    } finally {
      setIsThinking(false);
    }
  };

  // --------------------------------------------------
  // INITIAL LOAD + AUTO REFRESH
  // --------------------------------------------------

  useEffect(() => {
    fetchData();

    const interval =
      setInterval(() => {
        fetchData();
      }, 5000);

    return () => {
      clearInterval(interval);
    };
  }, []);

  // --------------------------------------------------
  // UI
  // --------------------------------------------------

  return (
    <div className="app">

      {/* Header */}
      <header className="header">

        <div>

          <h1>
            ⚡ AI Energy Monitoring
          </h1>

          <p>
            Smart Energy Monitoring & Analysis Assistant
          </p>

        </div>

        <div className="connection">

          <span
            className={`status-dot ${
              status?.connected
                ? "online"
                : "offline"
            }`}
          />

          {status?.connected
            ? "Meter Connected"
            : "Disconnected"}

        </div>

      </header>

      {/* Error */}
      {error !== "" && (
        <div className="error">
          {error}
        </div>
      )}

      <main className="dashboard">

        {/* Dashboard Header */}
        <section className="dashboard-header">

          <div>

            <h2>
              Energy Dashboard
            </h2>

            <p>
              Real-time electrical measurements from the
              smart meter.
            </p>

          </div>

          <button onClick={fetchData}>
            Refresh
          </button>

        </section>

        {/* Metric Cards */}
        <section className="metrics">

          <div className="metric-card">

            <span>Voltage</span>

            <strong>
              {telemetry?.voltage ?? "--"}
            </strong>

            <small>V</small>

          </div>

          <div className="metric-card">

            <span>Current</span>

            <strong>
              {telemetry?.current ?? "--"}
            </strong>

            <small>A</small>

          </div>

          <div className="metric-card">

            <span>Active Power</span>

            <strong>
              {telemetry?.active_power ?? "--"}
            </strong>

            <small>kW</small>

          </div>

          <div className="metric-card">

            <span>Power Factor</span>

            <strong>
              {telemetry?.power_factor ?? "--"}
            </strong>

            <small>PF</small>

          </div>

          <div className="metric-card">

            <span>Frequency</span>

            <strong>
              {telemetry?.frequency ?? "--"}
            </strong>

            <small>Hz</small>

          </div>

          <div className="metric-card">

            <span>Energy</span>

            <strong>
              {telemetry?.energy ?? "--"}
            </strong>

            <small>kWh</small>

          </div>

        </section>

        {/* Power Graph */}
        <section className="panel chart-panel">

          <div className="panel-header">

            <div>

              <h3>
                Power Consumption
              </h3>

              <p>
                Historical active power readings from PostgreSQL
              </p>

            </div>

            <div className="live-indicator">

              <span className="live-dot"></span>

              Live

            </div>

          </div>

          <div className="chart-container">

            <ResponsiveContainer
              width="100%"
              height="100%"
            >

              <LineChart
                data={powerHistory}
              >

                <CartesianGrid
                  strokeDasharray="3 3"
                />

                <XAxis
                  dataKey="time"
                />

                <YAxis />

                <Tooltip />

                <Line
                  type="monotone"
                  dataKey="power"
                  strokeWidth={3}
                  dot={false}
                />

              </LineChart>

            </ResponsiveContainer>

          </div>

        </section>

        {/* Details */}
        <section className="details">

          {/* Meter Information */}
          <div className="panel">

            <h3>
              Meter Information
            </h3>

            <div className="detail-row">

              <span>Meter ID</span>

              <strong>
                {status?.meter_id ?? "--"}
              </strong>

            </div>

            <div className="detail-row">

              <span>Connector</span>

              <strong>
                {status?.connector_type ?? "--"}
              </strong>

            </div>

            <div className="detail-row">

              <span>Status</span>

              <strong>
                {status?.connected
                  ? "Connected"
                  : "Disconnected"}
              </strong>

            </div>

          </div>

          {/* Electrical Details */}
          <div className="panel">

            <h3>
              Electrical Details
            </h3>

            <div className="detail-row">

              <span>Reactive Power</span>

              <strong>
                {telemetry?.reactive_power ?? "--"} kVAR
              </strong>

            </div>

            <div className="detail-row">

              <span>Apparent Power</span>

              <strong>
                {telemetry?.apparent_power ?? "--"} kVA
              </strong>

            </div>

            <div className="detail-row">

              <span>Demand</span>

              <strong>
                {telemetry?.demand ?? "--"} kW
              </strong>

            </div>

          </div>

          {/* AI Assistant */}
          <div className="panel ai-panel">

            <h3>
              🤖 AI Energy Assistant
            </h3>

            {!chatOpen ? (

              <div className="chat-placeholder">

                <div className="robot">
                  🤖
                </div>

                <h4>
                  Energy Assistant
                </h4>

                <p>
                  Ask questions about energy
                  consumption, meter readings and
                  system conditions.
                </p>

                <button
                  onClick={() => {
                    setChatOpen(true);
                  }}
                >
                  Start Chat
                </button>

              </div>

            ) : (

              <div className="chat-box">

                <div className="chat-messages">

                  {chatMessages.length === 0 && (

                    <div className="chat-message assistant">

                      🤖 Hello! I'm your Energy Assistant.

                      <br />

                      I use the latest energy analysis
                      from the system to answer your
                      questions.

                      <br />
                      <br />

                      Try asking:

                      <br />

                      • Is my system healthy?

                      <br />

                      • Why does the system need attention?

                      <br />

                      • Is power consumption increasing?

                      <br />

                      • What is the power trend?

                      <br />

                      • What is the average power?

                      <br />

                      • What is the voltage?

                      <br />

                      • Is the power factor good?

                      <br />

                      • Is the frequency normal?

                      <br />

                      • Is the meter connected?

                    </div>

                  )}

                  {chatMessages.map(
                    (chat, index) => (

                      <div
                        key={index}
                        className={`chat-message ${chat.sender}`}
                      >

                        {chat.sender === "user"
                          ? "You: "
                          : "🤖 "}

                        {chat.sender === "assistant" ? (
                          <ReactMarkdown>
                            {chat.text}
                          </ReactMarkdown>
                        ) : (
                          chat.text
                        )}

                      </div>

                    )
                  )}

                  {isThinking && (

                    <div className="chat-message assistant">

                      🤖 Analyzing the energy data...

                    </div>

                  )}

                </div>

                <div className="chat-input">

                  <input
                    type="text"
                    placeholder="Ask about your energy..."
                    value={message}
                    disabled={isThinking}
                    onChange={(event) => {
                      setMessage(
                        event.target.value
                      );
                    }}
                    onKeyDown={(event) => {

                      if (
                        event.key === "Enter" &&
                        !isThinking
                      ) {
                        handleChat();
                      }

                    }}
                  />

                  <button
                    onClick={handleChat}
                    disabled={isThinking}
                  >
                    {isThinking
                      ? "Thinking..."
                      : "Send"}
                  </button>

                </div>

              </div>

            )}

          </div>

        </section>

      </main>

    </div>
  );
}

export default App;