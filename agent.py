import os
import logging
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.agents import SequentialAgent

# Import tools we defined
from .tools import get_calendar_mcp_toolset, fetch_patient_medications

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

# --- 3. Primary Agent: Health Coordinator (Router/Triage) ---
root_agent = Agent(
    name="primary_health_coordinator",
    model=model_name,
    description="Primary triage agent that intercepts user queries and delegates to the right sub-agent.",
    instruction="""
    You are the AI Health Coordinator, the primary touchpoint for patients (accessible via WhatsApp or Web).
    You have a team of specialists to help you:
    1. 'booking_agent': Deals with Google Calendar appointments.
    2. 'medical_agent': Deals with lab reports, medications, and medical records.

    Triage the user's prompt. 
    If the prompt involves schedules or times, delegate to the 'booking_agent'.
    If the prompt involves checking prescriptions or lab results, delegate to the 'medical_agent'.
    If the prompt is general, provide a warm, empathetic greeting and ask how you can assist them today.
    """,
    sub_agents=[booking_agent, medical_agent]
)
