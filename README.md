# 🏥 AI Health Coordinator

An intelligent, multi-agent healthcare assistant built with **Google ADK** and **Gemini**. It acts as a primary touchpoint for patients — triaging queries and delegating to specialist sub-agents for appointment scheduling and medication management.
 
The system is composed of three agents working in concert:
- **`primary_health_coordinator`** — the root triage agent that intercepts all patient queries (via WhatsApp or Web) and routes them to the right specialist.
- **`booking_agent`** — handles appointment booking, rescheduling, and cancellations using Google Calendar via MCP.
- **`medical_agent`** — retrieves and explains patient medication schedules and lab records from Cloud Firestore, with a tone tailored for elderly patients.

---

## ✨ Features

- **Smart Triage** — A root agent intercepts all patient queries and routes them to the appropriate specialist.
- **Appointment Booking** — A dedicated sub-agent manages patient scheduling via Google Calendar (MCP integration).
- **Medication & Records Lookup** — A medical sub-agent retrieves patient medication plans from Google Cloud Firestore.
- **Multi-channel Ready** — Designed to be accessible via WhatsApp or a web interface.
- **Powered by Gemini** — Uses `gemini-2.5-flash` by default, configurable via environment variable.

---

## 🏗️ Architecture

```
primary_health_coordinator  (Root / Triage Agent)
├── booking_agent           (Appointment scheduling via Google Calendar MCP)
└── medical_agent           (Medication plans & lab records via Firestore)
```

The root agent (`primary_health_coordinator`) reads the patient's intent and delegates:
- Scheduling/time-related queries → `booking_agent`
- Prescription/medication/lab result queries → `medical_agent`
- General queries → Handled directly with a warm, empathetic response

---

## 📁 Project Structure

```
ai-health-coordinator/
├── agent.py          # Agent definitions (root + sub-agents)
├── tools.py          # Custom tool functions (calendar, Firestore)
├── __init__.py       # Package init
├── requirements.txt  # Python dependencies
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- A Google Cloud project with Firestore enabled
- A Gemini API key (via Google AI Studio or Vertex AI)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Aman3Ojha/ai-health-coordinator.git
   cd ai-health-coordinator
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root:

   ```env
   GOOGLE_CLOUD_PROJECT=your-gcp-project-id
   MODEL=gemini-2.5-flash   # Optional, this is the default
   ```

5. **Authenticate with Google Cloud**

   ```bash
   gcloud auth application-default login
   ```

---

## 🛠️ Tools
 
### Google ADK — `Agent` & `SequentialAgent`
The backbone of the multi-agent system. Each agent (`primary_health_coordinator`, `booking_agent`, `medical_agent`) is defined using `google.adk.Agent`, which handles model invocation, instruction-following, and tool dispatch. `SequentialAgent` from `google.adk.agents` is also imported for chaining agent steps when needed.
 
### Google ADK — `MCPToolset` + `StdioConnectionParams`
Used in `get_calendar_mcp_toolset()` (from `google.adk.tools.mcp_tool`) to connect the `booking_agent` to Google Calendar via the **Model Context Protocol (MCP)**. `StdioConnectionParams` establishes a stdio-based MCP connection, allowing the agent to communicate with external calendar tools as if they were native functions.
 
### Google Cloud Firestore
Used in `fetch_patient_medications()` via the `google.cloud.firestore` client. The `medical_agent` uses this tool to query the `patients` Firestore collection by `patient_id` and return the stored medication schedule to the patient in plain language.
 
### Gemini (`gemini-2.5-flash`)
All three agents run on Google's Gemini model, configurable via the `MODEL` environment variable. The default is `gemini-2.5-flash`, chosen for its speed and instruction-following quality in conversational healthcare contexts.
 
---
 
## 🔧 Configuration

| Environment Variable   | Description                              | Default             |
|------------------------|------------------------------------------|---------------------|
| `GOOGLE_CLOUD_PROJECT` | Your Google Cloud project ID             | *(required)*        |
| `MODEL`                | Gemini model to use for all agents       | `gemini-2.5-flash`  |

---

## 📦 Dependencies

| Package                  | Purpose                                  |
|--------------------------|------------------------------------------|
| `google-adk`             | Google Agent Development Kit             |
| `google-cloud-firestore` | Cloud Firestore client for patient data  |

---

## 🗂️ Firestore Data Schema

The `medical_agent` expects a Firestore collection structured as:

```
patients/
└── {patient_id}/
    └── medications: ["Metformin 500mg twice daily", "Atorvastatin 10mg at night"]
```

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## ⚠️ Disclaimer

This project is intended for educational and demonstration purposes. It is **not** a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical decisions.

---

## 📄 License

This project is open-source. See the [LICENSE](LICENSE) file for details.
