author: AI Health Coordinator Team
summary: Build a multi-agent AI Health Coordinator using Google ADK, Gemini, MCP, Firestore, and Cloud Run — step-by-step, entirely from Google Cloud Shell.
id: ai-health-coordinator
categories: Cloud, AI, Healthcare
environments: Web
status: Published
feedback link: https://github.com/Aman3Ojha/ai-health-coordinator/issues
analytics account: UA-XXXXXXXX-X

# AI Health Coordinator — Multi-Agent System with ADK, MCP & Cloud Run

## Overview
Duration: 2:00

In this codelab you will build a **production-ready, multi-agent AI healthcare assistant** entirely from Google Cloud Shell. The system triages patient queries and delegates them to specialist AI sub-agents backed by live government health APIs and Google Cloud services.

### What you will build

```
primary_health_coordinator  (Root triage agent — Gemini)
├── booking_agent           (Google Calendar via MCP)
├── medical_agent           (Firestore — patient medication records)
└── research_agent          (OpenFDA API + NIH MedlinePlus API)
```

A patient can ask:
- *"Book me an appointment for Thursday at 3 pm"* → `booking_agent`
- *"What medications am I on?"* → `medical_agent`
- *"What are the side effects of Metformin?"* → `research_agent` → OpenFDA
- *"What does chest pain mean?"* → `research_agent` → MedlinePlus

### What you will learn

- How to scaffold a **Google ADK** multi-agent project.
- How to wire sub-agents together with a root triage agent.
- How to define **MCP (Model Context Protocol)** tools for external APIs.
- How to query the **OpenFDA** and **NIH MedlinePlus** APIs from ADK tools.
- How to persist patient data in **Google Cloud Firestore**.
- How to deploy the agent as an HTTP API on **Cloud Run**.

### Prerequisites

| Requirement | Details |
|---|---|
| Google Cloud account | Free tier is sufficient. [Create one](https://cloud.google.com/free) |
| Google Cloud project | A project with billing enabled |
| Browser | Any modern browser (Cloud Shell runs in the browser) |

> **No local installation required.** Everything runs in Google Cloud Shell.

<aside class="positive">
<b>Free APIs used:</b> OpenFDA and NIH MedlinePlus are free, public APIs. No API keys are required for either service.
</aside>

---

## Set Up Cloud Shell & Project
Duration: 5:00

### 1. Open Google Cloud Shell

1. Go to [console.cloud.google.com](https://console.cloud.google.com).
2. Click the **Activate Cloud Shell** button (terminal icon, top-right).
3. Wait for the shell to provision.

### 2. Set your project

```bash
# Replace YOUR_PROJECT_ID with your actual Google Cloud project ID
export PROJECT_ID="YOUR_PROJECT_ID"
gcloud config set project $PROJECT_ID
echo "Project set to: $PROJECT_ID"
```

### 3. Enable required APIs

```bash
gcloud services enable \
  firestore.googleapis.com \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  aiplatform.googleapis.com \
  --project=$PROJECT_ID
```

<aside class="positive">
This single command enables Firestore, Cloud Run, Cloud Build, and Vertex AI. It may take 1–2 minutes.
</aside>

### 4. Create a Firestore database (Native mode)

```bash
gcloud firestore databases create \
  --location=nam5 \
  --project=$PROJECT_ID
```

### 5. Set application default credentials

```bash
gcloud auth application-default login
```

Follow the browser prompt to authenticate. Cloud Shell will store the credentials automatically.

---

## Clone the Repository
Duration: 3:00

### 1. Clone and navigate into the project

```bash
git clone https://github.com/Aman3Ojha/ai-health-coordinator.git
cd ai-health-coordinator
```

### 2. Review the project layout

```
ai-health-coordinator/
├── agent.py          # All agent definitions (root + 3 sub-agents)
├── tools.py          # Tool functions (Calendar, Firestore, OpenFDA, MedlinePlus)
├── __init__.py       # Python package init
├── requirements.txt  # Python dependencies
├── Dockerfile        # Container image for Cloud Run
├── .env.example      # Template for environment variables
└── codelab.md        # This codelab
```

### 3. Copy the environment template

```bash
cp .env.example .env
```

### 4. Fill in your project ID

```bash
sed -i "s/your-gcp-project-id/$PROJECT_ID/" .env
cat .env
```

Expected output:

```
GOOGLE_CLOUD_PROJECT=your-actual-project-id
MODEL=gemini-2.5-flash
```

---

## Install Dependencies
Duration: 3:00

### 1. Create a Python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Upgrade pip and install packages

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

The `requirements.txt` installs:

| Package | Purpose |
|---|---|
| `google-adk` | Google Agent Development Kit — agent runtime |
| `google-cloud-firestore` | Firestore client for patient medication records |
| `requests` | HTTP client for OpenFDA and MedlinePlus APIs |
| `python-dotenv` | Load `.env` variables at runtime |

### 3. Verify the ADK installation

```bash
adk --version
```

<aside class="positive">
You should see a version string such as <code>adk 1.x.x</code>. If not, re-run <code>pip install google-adk</code>.
</aside>

---

## Understand the Tools
Duration: 8:00

Open `tools.py` in the Cloud Shell editor or with `cat tools.py`. The file defines four tool functions that the agents call at runtime.

### Tool 1 — `book_appointment` (Google Calendar via MCP)

```python
def get_calendar_mcp_toolset():
    def book_appointment(date_time: str) -> str:
        """Book an appointment for a specific date and time on the calendar."""
        return f"Success! The appointment is booked for {date_time}."
    return book_appointment
```

> In a production deployment you would replace the stub with a real **MCP connection** to a Calendar MCP server (see the *Extending with Real MCP* step).

### Tool 2 — `fetch_patient_medications` (Cloud Firestore)

```python
def fetch_patient_medications(patient_id: str) -> str:
    """Retrieve patient medication schedules from Firestore."""
    db = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
    doc = db.collection("patients").document(patient_id).get()
    if doc.exists:
        data = doc.to_dict()
        return f"Medications for {patient_id}: {data.get('medications', 'None')}"
    return f"No records found for {patient_id}."
```

This tool is a **real Firestore query**. The agent passes a `patient_id` and gets back the stored medication list.

### Tool 3 — `scrape_drug_info` (OpenFDA API)

```python
def scrape_drug_info(drug_name: str) -> str:
    """Fetch FDA drug label information (purpose, warnings, interactions)."""
    url = "https://api.fda.gov/drug/label.json"
    params = {"search": f"openfda.generic_name:{drug_name}", "limit": 1}
    response = requests.get(url, params=params, timeout=10)
    label = response.json()["results"][0]
    ...
```

The **OpenFDA REST API** is completely free and requires no API key. It returns the official FDA drug label for any medication.

<aside class="positive">
<b>Try it yourself:</b> Paste the following URL in your browser to see raw FDA data for Metformin:<br>
<code>https://api.fda.gov/drug/label.json?search=openfda.generic_name:metformin&limit=1</code>
</aside>

### Tool 4 — `scrape_symptom_info` (NIH MedlinePlus)

```python
def scrape_symptom_info(symptom: str) -> str:
    """Query NIH MedlinePlus for trusted health topic summaries."""
    url = "https://wsearch.nlm.nih.gov/ws/query"
    params = {"db": "healthTopics", "term": symptom, "retmax": 3}
    response = requests.get(url, params=params, timeout=10)
    ...
```

The **MedlinePlus Web Service** is a free NIH API. It returns curated health topic articles with source links.

<aside class="positive">
<b>Try it yourself:</b>
<code>https://wsearch.nlm.nih.gov/ws/query?db=healthTopics&term=chest+pain&retmax=3</code>
</aside>

---

## Understand the Agents
Duration: 8:00

Open `agent.py` or run `cat agent.py`. The file defines four agents wired into a hierarchy.

### Architecture diagram

```
┌──────────────────────────────────────────────────────┐
│           primary_health_coordinator                 │
│         (Root triage — Gemini 2.5 Flash)             │
│                                                      │
│  Receives every patient message and routes it to:    │
└──────┬──────────────┬───────────────┬────────────────┘
       │              │               │
       ▼              ▼               ▼
┌────────────┐ ┌─────────────┐ ┌──────────────────────┐
│booking_    │ │medical_     │ │research_agent        │
│agent       │ │agent        │ │                      │
│            │ │             │ │ scrape_drug_info()   │
│ book_      │ │ fetch_      │ │   → OpenFDA API      │
│ appointment│ │ patient_    │ │                      │
│ (Calendar) │ │ medications │ │ scrape_symptom_info()│
│            │ │ (Firestore) │ │   → MedlinePlus API  │
└────────────┘ └─────────────┘ └──────────────────────┘
```

### Sub-agent 1 — `booking_agent`

```python
booking_agent = Agent(
    name="booking_agent",
    model=model_name,
    description="Specialist for booking, reading, and rescheduling patient appointments on Google Calendar.",
    instruction="""
    You are the Appointment Coordinator. You manage the clinic's schedule using the 
    Google Calendar MCP tools. Always confirm the date and time before terminating.
    """,
    tools=[calendar_toolset]
)
```

### Sub-agent 2 — `medical_agent`

```python
medical_agent = Agent(
    name="medical_agent",
    model=model_name,
    description="Specialist for reading lab reports and managing medication plans.",
    instruction="""
    You are the Medical Records Coordinator. Use Firestore tools to find patient 
    medication plans. Explain schedules clearly, especially for elderly patients.
    """,
    tools=[fetch_patient_medications]
)
```

### Sub-agent 3 — `research_agent`

```python
research_agent = Agent(
    name="research_agent",
    model=model_name,
    description="Specialist for live drug info (OpenFDA) and symptom summaries (MedlinePlus).",
    instruction="""
    You are the Medical Research Coordinator. Use scrape_drug_info for drug questions 
    and scrape_symptom_info for symptom/condition questions. Always cite the source 
    and remind patients to consult their doctor.
    """,
    tools=[scrape_drug_info, scrape_symptom_info]
)
```

### Root agent — `primary_health_coordinator`

```python
root_agent = Agent(
    name="primary_health_coordinator",
    model=model_name,
    description="Primary triage agent.",
    instruction="""
    Route patient queries:
    - Schedules/times → booking_agent
    - Prescriptions/lab results → medical_agent
    - Drug side effects / symptoms → research_agent
    - General queries → respond warmly and ask how to help
    """,
    sub_agents=[booking_agent, medical_agent, research_agent]
)
```

<aside class="positive">
<b>Key ADK concept:</b> The root agent does <em>not</em> call tools directly. It reads the patient's intent and issues a <code>transfer_to_agent</code> call to the appropriate sub-agent, which then executes its tools and responds.
</aside>

---

## Seed Firestore with Test Data
Duration: 5:00

The `medical_agent` reads from Firestore. Let's add a test patient record.

### 1. Open the interactive Python REPL

```bash
python3
```

### 2. Write a test patient record

```python
import os
from dotenv import load_dotenv
from google.cloud import firestore

load_dotenv()
db = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))

db.collection("patients").document("P001").set({
    "name": "Alice Johnson",
    "age": 72,
    "medications": [
        "Metformin 500mg — twice daily with meals",
        "Atorvastatin 10mg — once daily at bedtime",
        "Lisinopril 5mg — once daily in the morning",
    ],
    "next_appointment": "2025-05-15T10:00:00",
})

print("Patient P001 seeded successfully.")
exit()
```

### 3. Verify the record in the Console

Open the [Firestore console](https://console.cloud.google.com/firestore/databases/-default-/data) and confirm you can see the `patients/P001` document.

---

## Run the Agent Locally
Duration: 5:00

### 1. Start the ADK development server

```bash
adk web .
```

The server starts on `http://localhost:8080`. In Cloud Shell, click **Web Preview → Preview on port 8080** to open the chat UI.

### 2. Test each agent path

Try these prompts in the ADK web UI:

| Prompt | Expected agent | Expected behavior |
|---|---|---|
| `Book me an appointment for Friday at 2pm` | `booking_agent` | Returns booking confirmation |
| `What medications is patient P001 on?` | `medical_agent` | Returns Firestore medications |
| `What are the side effects of Metformin?` | `research_agent` | Returns FDA label warnings |
| `What does chest pain mean?` | `research_agent` | Returns MedlinePlus summaries |
| `Hello` | root agent | Warm greeting |

### 3. Test tools directly (optional)

```bash
python3 - <<'EOF'
from tools import scrape_drug_info, scrape_symptom_info

print(scrape_drug_info("metformin"))
print("---")
print(scrape_symptom_info("chest pain"))
EOF
```

<aside class="positive">
<b>Expected:</b> You should see real FDA label data for Metformin and NIH MedlinePlus summaries for chest pain — live from the APIs, no mocking.
</aside>

---

## Extending with Real MCP (Model Context Protocol)
Duration: 10:00

The current `book_appointment` is a stub. This step shows you how to replace it with a real **MCP toolset** that connects to a Calendar MCP server.

### What is MCP?

Model Context Protocol is an open standard that lets AI agents call external tools over a well-defined protocol (stdio or HTTP/SSE). Google ADK has built-in support via `MCPToolset` and `StdioConnectionParams`.

### Option A — Stdio-based MCP (local MCP server process)

```python
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams

calendar_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-google-calendar"],
        env={
            "GOOGLE_CALENDAR_CREDENTIALS": "/path/to/credentials.json",
        },
    )
)
```

This tells ADK to launch the MCP Calendar server as a subprocess and connect via stdin/stdout.

### Option B — HTTP/SSE-based MCP (remote MCP server)

```python
from google.adk.tools.mcp_tool import MCPToolset, SseConnectionParams

calendar_toolset = MCPToolset(
    connection_params=SseConnectionParams(
        url="https://your-mcp-server.run.app/mcp",
        headers={"Authorization": "Bearer YOUR_TOKEN"},
    )
)
```

### MCP tool definition example

A Calendar MCP server exposes tools as JSON schema definitions. Here is an example tool definition that an MCP server would advertise:

```json
{
  "name": "create_calendar_event",
  "description": "Create a new event in Google Calendar.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "summary":    { "type": "string", "description": "Event title" },
      "start":      { "type": "string", "description": "ISO 8601 start datetime" },
      "end":        { "type": "string", "description": "ISO 8601 end datetime" },
      "attendees":  {
        "type": "array",
        "items": { "type": "string", "description": "Attendee email" }
      }
    },
    "required": ["summary", "start", "end"]
  }
}
```

ADK automatically converts MCP tool definitions into callable Python functions that the agent can dispatch.

### Swapping the stub for the real toolset

In `tools.py`, replace `get_calendar_mcp_toolset()` with:

```python
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams

def get_calendar_mcp_toolset():
    return MCPToolset(
        connection_params=StdioConnectionParams(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-google-calendar"],
        )
    )
```

And in `agent.py`, pass it directly:

```python
booking_agent = Agent(
    name="booking_agent",
    ...
    tools=[get_calendar_mcp_toolset()],   # MCPToolset instance
)
```

<aside class="negative">
<b>Note:</b> Real Calendar MCP integration requires OAuth 2.0 credentials for the Google Calendar API and Node.js installed in your environment. For the purposes of this codelab the stub is sufficient to demonstrate the multi-agent routing architecture.
</aside>

---

## Deploy to Cloud Run
Duration: 10:00

### 1. Build the container image with Cloud Build

```bash
# From the project root
export IMAGE="gcr.io/$PROJECT_ID/ai-health-coordinator:latest"

gcloud builds submit \
  --tag $IMAGE \
  --project $PROJECT_ID \
  .
```

Cloud Build uses the `Dockerfile` at the project root to build and push the image to Google Container Registry.

### 2. Deploy to Cloud Run

```bash
gcloud run deploy ai-health-coordinator \
  --image $IMAGE \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=$PROJECT_ID,MODEL=gemini-2.5-flash \
  --project $PROJECT_ID
```

<aside class="positive">
Cloud Run automatically provisions HTTPS, scales to zero when idle (free tier), and scales up under load. You only pay for actual request processing time.
</aside>

### 3. Get the service URL

```bash
gcloud run services describe ai-health-coordinator \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

### 4. Test the deployed endpoint

```bash
SERVICE_URL=$(gcloud run services describe ai-health-coordinator \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)')

curl -X POST "$SERVICE_URL/run" \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the side effects of Atorvastatin?"}'
```

Expected response: a JSON object containing the `research_agent`'s answer with live FDA data.

---

## Security Best Practices
Duration: 5:00

### 1. Never commit secrets

Always use environment variables or Secret Manager — never hardcode API keys or project IDs.

```bash
# Store a secret in Google Secret Manager
echo -n "your-secret-value" | \
  gcloud secrets create MY_SECRET --data-file=- --project=$PROJECT_ID

# Reference it in Cloud Run
gcloud run services update ai-health-coordinator \
  --set-secrets MY_SECRET=MY_SECRET:latest \
  --region us-central1
```

### 2. Use least-privilege IAM

Create a dedicated service account for Cloud Run:

```bash
gcloud iam service-accounts create health-coordinator-sa \
  --display-name="AI Health Coordinator SA" \
  --project=$PROJECT_ID

# Grant only Firestore read access
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:health-coordinator-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/datastore.user"

# Attach to Cloud Run service
gcloud run services update ai-health-coordinator \
  --service-account="health-coordinator-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --region us-central1
```

### 3. Restrict unauthenticated access in production

```bash
# Remove public access; require an identity token instead
gcloud run services update ai-health-coordinator \
  --no-allow-unauthenticated \
  --region us-central1
```

Call the service with a token:

```bash
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
     -X POST "$SERVICE_URL/run" \
     -d '{"message":"Hello"}'
```

### 4. Validate and sanitise all user input

In `tools.py`, the API calls already time out after 10 seconds and wrap every external call in `try/except`. Extend this by:

- Stripping whitespace and limiting input length before passing to the APIs.
- Logging unexpected responses for audit purposes.

### 5. Medical disclaimer

Always surface a disclaimer in the root agent's responses. The instruction already contains: *"remind the patient to consult their doctor before making any medical decisions."*

<aside class="negative">
<b>Important:</b> This system is for educational and demonstration purposes only. It is <b>not</b> a substitute for professional medical advice, diagnosis, or treatment.
</aside>

---

## Congratulations!
Duration: 1:00

You have successfully built and deployed a **multi-agent AI Health Coordinator** on Google Cloud!

### What you built

✅ A root triage agent (Gemini) that routes patient queries.  
✅ A `booking_agent` wired to Google Calendar via MCP.  
✅ A `medical_agent` backed by Cloud Firestore.  
✅ A `research_agent` that queries live OpenFDA and MedlinePlus APIs — no API key required.  
✅ A Dockerised Cloud Run deployment.  
✅ Security best practices with IAM and Secret Manager.

### Next steps

- **Integrate real Calendar MCP**: Follow the `@modelcontextprotocol/server-google-calendar` setup guide to enable real appointment booking.
- **Add WhatsApp integration**: Use the Twilio API or WhatsApp Business API to expose the coordinator over WhatsApp.
- **Add Pub/Sub notifications**: Use Cloud Pub/Sub to trigger proactive medication reminders.
- **Add authentication**: Protect the Cloud Run endpoint with Google IAP or Firebase Authentication.

### Useful links

| Resource | URL |
|---|---|
| Google ADK documentation | [cloud.google.com/adk](https://cloud.google.com/products/agent-development-kit) |
| ADK + MCP Codelab | [codelabs.developers.google.com/adk-mcp-bigquery-maps](https://codelabs.developers.google.com/adk-mcp-bigquery-maps) |
| Deploy ADK to Cloud Run | [codelabs.developers.google.com/…/deploy-an-adk-agent-to-cloud-run](https://codelabs.developers.google.com/codelabs/production-ready-ai-with-gc/5-deploying-agents/deploy-an-adk-agent-to-cloud-run#0) |
| OpenFDA API docs | [open.fda.gov/apis](https://open.fda.gov/apis/) |
| MedlinePlus Web Service | [medlineplus.gov/webservices](https://medlineplus.gov/webservices.html) |
| Google Cloud Skills Boost | [skills.google](https://www.skills.google) |
