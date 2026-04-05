# 🏥 AI Health Coordinator

An intelligent, multi-agent healthcare assistant built with **Google ADK** and **Gemini**. It acts as a primary touchpoint for patients — triaging queries and delegating to specialist sub-agents for appointment scheduling and medication management.

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

### `book_appointment(date_time: str)`
Books a patient appointment for a specified date and time on Google Calendar.

### `fetch_patient_medications(patient_id: str)`
Fetches a patient's medication schedule from Cloud Firestore.
- Looks up the `patients` collection by `patient_id`
- Returns the `medications` field if found

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
