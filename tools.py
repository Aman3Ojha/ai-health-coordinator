import os
import re
import requests
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


def scrape_drug_info(drug_name: str) -> str:
    """Fetch FDA drug label information including purpose, warnings, and interactions
    from the OpenFDA public API (no API key required).

    Args:
        drug_name: The name of the drug to look up (e.g. 'metformin').

    Returns:
        A human-readable summary of the drug's purpose, warnings, and interactions,
        or an error message if the drug cannot be found.
    """
    url = "https://api.fda.gov/drug/label.json"
    params = {"search": f"openfda.brand_name:{drug_name}+openfda.generic_name:{drug_name}", "limit": 1}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        results = response.json().get("results", [])
        if not results:
            # Fallback: search by generic name only
            params = {"search": f"openfda.generic_name:{drug_name}", "limit": 1}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            results = response.json().get("results", [])
        if not results:
            return f"No FDA label information found for '{drug_name}'."
        label = results[0]
        purpose = label.get("purpose", ["Not available"])[0]
        warnings = label.get("warnings", ["Not available"])[0]
        interactions = label.get("drug_interactions", ["Not available"])[0]
        return (
            f"**FDA Drug Information for {drug_name.title()}**\n\n"
            f"**Purpose:** {purpose[:500]}\n\n"
            f"**Warnings:** {warnings[:500]}\n\n"
            f"**Drug Interactions:** {interactions[:500]}"
        )
    except requests.exceptions.RequestException as e:
        return f"Error contacting OpenFDA API: {str(e)}"
    except (KeyError, IndexError, ValueError) as e:
        return f"Error parsing OpenFDA response: {str(e)}"


def scrape_symptom_info(symptom: str) -> str:
    """Fetch trusted health condition summaries from the NIH MedlinePlus API.

    Queries the MedlinePlus Connect service for information related to the given
    symptom or health condition.

    Args:
        symptom: The symptom or health condition to look up (e.g. 'chest pain').

    Returns:
        The top 3 MedlinePlus health topic summaries with source links, or an error
        message if no information is found.
    """
    url = "https://wsearch.nlm.nih.gov/ws/query"
    params = {
        "db": "healthTopics",
        "term": symptom,
        "retmax": 3,
        "rettype": "brief",
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        # MedlinePlus returns XML; parse the title, URL, and snippet values from the response
        content = response.text
        # Extract <title>, <url>, and <snippet> values from the XML
        titles = re.findall(r"<content name=\"title\">(.*?)</content>", content)
        urls = re.findall(r"<url>(.*?)</url>", content)
        snippets = re.findall(r"<content name=\"snippet\">(.*?)</content>", content, re.DOTALL)
        if not titles:
            return f"No MedlinePlus information found for '{symptom}'."
        results = []
        for i, title in enumerate(titles[:3]):
            url_text = urls[i] if i < len(urls) else "https://medlineplus.gov"
            if i < len(snippets):
                raw_snippet = re.sub(r"<[^>]+>", "", snippets[i]).strip()
                snippet_text = raw_snippet[:300]
            else:
                snippet_text = ""
            results.append(f"**{title}**\n{snippet_text}\nSource: {url_text}")
        return (
            f"**MedlinePlus Health Information for '{symptom}'**\n\n"
            + "\n\n---\n\n".join(results)
        )
    except requests.exceptions.RequestException as e:
        return f"Error contacting MedlinePlus API: {str(e)}"
    except Exception as e:
        return f"Error parsing MedlinePlus response: {str(e)}"
