# 🏥 AI Health Coordinator

An intelligent, multi-agent healthcare assistant built with **Google ADK** and **Gemini**. It acts as a primary touchpoint for patients — triaging queries and delegating to specialist sub-agents for appointment scheduling, medication management, and live medical research.

The system is composed of four agents working in concert:

- **`primary_health_coordinator`** — the root triage agent that intercepts all patient queries (via WhatsApp or Web) and routes them to the right specialist.
- **`booking_agent`** — handles appointment booking, rescheduling, and cancellations using Google Calendar via MCP.
- **`medical_agent`** — retrieves and explains patient medication schedules and lab records from Cloud Firestore, with a tone tailored for elderly patients.
- **`research_agent`** — answers drug and symptom questions using live data from the **OpenFDA API** (FDA drug labels, warnings, interactions) and the **NIH MedlinePlus API** (health topic summaries).

---

## ✨ Features

- **Smart Triage** — A root agent intercepts all patient queries and routes them to the appropriate specialist.
- **Appointment Booking** — A dedicated sub-agent manages patient scheduling via Google Calendar (MCP integration).
- **Medication & Records Lookup** — A medical sub-agent retrieves patient medication plans from Google Cloud Firestore.
- **Live Medical Research** — A research sub-agent queries the free OpenFDA and NIH MedlinePlus APIs for drug information and symptom summaries — no API key required.
- **Multi-channel Ready** — Designed to be accessible via WhatsApp or a web interface.
- **Powered by Gemini** — Uses `gemini-2.5-flash` by default, configurable via environment variable.
- **Cloud Run Deployment** — Fully containerised, ready to deploy with a single `gcloud run deploy` command.

---

## 🏗️ Architecture

```
primary_health_coordinator  (Root / Triage Agent — Gemini)
├── booking_agent           (Appointment scheduling via Google Calendar MCP)
├── medical_agent           (Medication plans & lab records via Firestore)
└── research_agent          (Live drug info via OpenFDA + symptom info via MedlinePlus)
```

The root agent (`primary_health_coordinator`) reads the patient's intent and delegates:

| Patient query | Routed to |
|---|---|
| *"Book me an appointment for Thursday"* | `booking_agent` |
| *"What medications am I on?"* | `medical_agent` |
| *"What are the side effects of Metformin?"* | `research_agent` → OpenFDA |
| *"What does chest pain mean?"* | `research_agent` → MedlinePlus |
| *"Hello"* | Root agent (warm greeting) |

---

## 📁 Project Structure

```
ai-health-coordinator/
├── agent.py          # Agent definitions (root + 3 sub-agents)
├── tools.py          # Tool functions (Calendar, Firestore, OpenFDA, MedlinePlus)
├── __init__.py       # Package init
├── requirements.txt  # Python dependencies
├── Dockerfile        # Container image for Cloud Run deployment
├── .env.example      # Template for environment variables
└── codelab.md        # Step-by-step Google Codelab tutorial
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

   ```bash
   cp .env.example .env
   # Edit .env and fill in your GOOGLE_CLOUD_PROJECT
   ```

   ```env
   GOOGLE_CLOUD_PROJECT=your-gcp-project-id
   MODEL=gemini-2.5-flash   # Optional, this is the default
   ```

5. **Authenticate with Google Cloud**

   ```bash
   gcloud auth application-default login
   ```

6. **Run the ADK development server**

   ```bash
   adk web .
   ```

---

## 📖 Step-by-Step Codelab

For a complete, beginner-friendly walkthrough covering Cloud Shell setup, Firestore seeding, local testing, MCP integration, Cloud Run deployment, and security best practices, follow the **[`codelab.md`](./codelab.md)** in this repository.

---

## 🛠️ Tools

### Google ADK — `Agent`
The backbone of the multi-agent system. Each agent is defined using `google.adk.Agent`, which handles model invocation, instruction-following, and tool dispatch.

### Google ADK — `MCPToolset` + `StdioConnectionParams`
Used in `get_calendar_mcp_toolset()` (from `google.adk.tools.mcp_tool`) to connect the `booking_agent` to Google Calendar via the **Model Context Protocol (MCP)**. `StdioConnectionParams` establishes a stdio-based MCP connection.

### Google Cloud Firestore
Used in `fetch_patient_medications()` via the `google.cloud.firestore` client. The `medical_agent` queries the `patients` Firestore collection by `patient_id`.

### OpenFDA API (`scrape_drug_info`)
A **free, public REST API** (no key required) that returns official FDA drug labels. Used by the `research_agent` to answer questions about drug side effects, warnings, and interactions.

### NIH MedlinePlus API (`scrape_symptom_info`)
A **free NIH Web Service** that returns curated health topic summaries. Used by the `research_agent` to answer symptom and medical condition questions.

### Gemini (`gemini-2.5-flash`)
All four agents run on Google's Gemini model, configurable via the `MODEL` environment variable.

---

## 🔧 Configuration

| Environment Variable   | Description                              | Default             |
|------------------------|------------------------------------------|---------------------|
| `GOOGLE_CLOUD_PROJECT` | Your Google Cloud project ID             | *(required)*        |
| `MODEL`                | Gemini model to use for all agents       | `gemini-2.5-flash`  |

---

## 📦 Dependencies

| Package                  | Purpose                                             |
|--------------------------|-----------------------------------------------------|
| `google-adk`             | Google Agent Development Kit                        |
| `google-cloud-firestore` | Cloud Firestore client for patient data             |
| `requests`               | HTTP client for OpenFDA and MedlinePlus API calls   |
| `python-dotenv`          | Load `.env` environment variables at runtime        |

---

## 🗂️ Firestore Data Schema

The `medical_agent` expects a Firestore collection structured as:

```
patients/
└── {patient_id}/
    ├── name: "Alice Johnson"
    ├── age: 72
    ├── medications: ["Metformin 500mg twice daily", "Atorvastatin 10mg at night"]
    └── next_appointment: "2025-05-15T10:00:00"
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

