from typing import Dict
from src.main import RecruiterAssistant

# Simple in-memory store (OK for MVP)
SESSIONS: Dict[str, RecruiterAssistant] = {}

def get_assistant(phone_number: str, first_name: str | None = None) -> RecruiterAssistant:
    if phone_number not in SESSIONS:
        assistant = RecruiterAssistant(first_name or "Candidate")
        assistant.start()
        SESSIONS[phone_number] = assistant
    return SESSIONS[phone_number]
