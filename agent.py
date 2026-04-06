import os
import logging
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.agents import SequentialAgent

# Import tools we defined
from .tools import (
    get_calendar_mcp_toolset,
    fetch_patient_medications,
    scrape_drug_info,
    scrape_symptom_info,
)

load_dotenv()
model_name = os.getenv("MODEL", "gemini-2.5-flash")
logging.basicConfig(level=logging.INFO)

# --- 1. Sub-Agent: Appointment Booking ---
calendar_toolset = get_calendar_mcp_toolset()

booking_agent = Agent(
    name="booking_agent",
    model=model_name,
    description="Specialist for booking, reading, and rescheduling patient appointments on Google Calendar.",
    instruction="""
    You are the Appointment Coordinator. You manage the clinic's schedule using the Google Calendar MCP tools.
    If a patient wants to book, reschedule, or cancel, use your calendar tools. 
    Always confirm the date and time cleanly before terminating.
    """,
    tools=[calendar_toolset]
)

# --- 2. Sub-Agent: Medical Records & Triage ---
medical_agent = Agent(
    name="medical_agent",
    model=model_name,
    description="Specialist for reading lab reports, summarizing medical instructions, and managing medication plans.",
    instruction="""
    You are the Medical Records Coordinator. Use your database tools to find patient medication plans.
    Explain the medication schedule to the patient clearly and simply, keeping it empathetic to elderly patients.
    """,
    tools=[fetch_patient_medications]
)

# --- 3. Sub-Agent: Research (OpenFDA + MedlinePlus) ---
research_agent = Agent(
    name="research_agent",
    model=model_name,
    description=(
        "Specialist for live medical research: drug information (side effects, warnings, "
        "interactions) from OpenFDA and symptom/condition summaries from NIH MedlinePlus."
    ),
    instruction="""
    You are the Medical Research Coordinator. You have access to two live data sources:
    1. 'scrape_drug_info(drug_name)' — queries the OpenFDA public API for official FDA drug
       labels, warnings, and known drug interactions.
    2. 'scrape_symptom_info(symptom)' — queries NIH MedlinePlus for trusted health topic
       summaries about symptoms and medical conditions.

    Use these tools when a patient asks about:
    - Side effects, warnings, or interactions for any medication.
    - What a symptom or health condition means.
    - General drug information (purpose, dosage notes).

    Always cite the source (FDA / MedlinePlus) and remind the patient to consult their
    doctor before making any medical decisions.
    """,
    tools=[scrape_drug_info, scrape_symptom_info]
)

# --- 4. Primary Agent: Health Coordinator (Router/Triage) ---
root_agent = Agent(
    name="primary_health_coordinator",
    model=model_name,
    description="Primary triage agent that intercepts user queries and delegates to the right sub-agent.",
    instruction="""
    You are the AI Health Coordinator, the primary touchpoint for patients (accessible via WhatsApp or Web).
    You have a team of specialists to help you:
    1. 'booking_agent': Deals with Google Calendar appointments.
    2. 'medical_agent': Deals with lab reports, medications, and medical records from Firestore.
    3. 'research_agent': Answers questions about drug side effects, warnings, interactions, and
       symptom information using live OpenFDA and MedlinePlus data.

    Triage the user's prompt:
    - If the prompt involves schedules or times, delegate to 'booking_agent'.
    - If the prompt involves checking prescriptions or lab results, delegate to 'medical_agent'.
    - If the prompt asks about drug side effects, warnings, interactions, or symptoms/conditions,
      delegate to 'research_agent'.
    - If the prompt is general, provide a warm, empathetic greeting and ask how you can assist
      them today.
    """,
    sub_agents=[booking_agent, medical_agent, research_agent]
)
