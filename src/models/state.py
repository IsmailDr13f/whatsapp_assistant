"""
State and data models for the Recruiter Assistant.
"""
from typing import TypedDict, Optional, List, Dict
from pydantic import BaseModel


class RecruiterState(TypedDict):
    """Main state for the recruiter conversation flow."""
    first_name: str
    meeting_booked: Optional[bool]
    permission_given: Optional[bool]
    messages: List[Dict[str, str]]
    log: List[str]
    
    # Question responses
    in_morocco: Optional[bool]
    current_city: Optional[str]
    plan_to_move: Optional[str]
    preferred_cities: Optional[str]
    has_call_center_experience: Optional[bool]
    experience_details: Optional[str]
    why_call_center: Optional[str]
    salary_expectation: Optional[str]
    previous_applications: Optional[str]
    
    # Current question tracker
    current_question: Optional[str]


class YesNoIntent(BaseModel):
    """Intent classification result for yes/no questions."""
    answer: Optional[bool]  # true/false/null
    confidence: float
    reasoning: str