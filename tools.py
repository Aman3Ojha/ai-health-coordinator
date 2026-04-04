import os
from google.cloud import firestore
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams
def get_calendar_mcp_toolset():
    def book_appointment(date_time: str) -> str:
        """Book an appointment for a specific date and time on the calendar."""
        return f"Success! The appointment is booked for {date_time}."
    return book_appointment


def fetch_patient_medications(patient_id: str) -> str:
    """A custom tool to retrieve patient medication schedules from Firestore."""
    db = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
    try:
        doc = db.collection("patients").document(patient_id).get()
        if doc.exists:
            data = doc.to_dict()
            return f"Medications for {patient_id}: {data.get('medications', 'None')}"
        return f"No records found for {patient_id}."
    except Exception as e:
        return f"Database error: {str(e)}"
