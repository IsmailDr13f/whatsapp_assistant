"""
Questionnaire nodes for collecting candidate information.
"""
from config.settings import settings
from src.models.state import RecruiterState


def question_location(state: RecruiterState) -> RecruiterState:
    """
    Ask if candidate is currently in Morocco.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with location question
    """
    msg = settings.QUESTIONS["location"]
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Asked: Location (in Morocco?)")
    state["current_question"] = "location"
    return state


def question_city(state: RecruiterState) -> RecruiterState:
    """
    Ask which city the candidate is currently in.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with city question
    """
    msg = settings.QUESTIONS["city"]
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Asked: Current city")
    state["current_question"] = "city"
    return state


def question_plan_to_move(state: RecruiterState) -> RecruiterState:
    """
    Ask about plans to move to Morocco.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with plan to move question
    """
    msg = settings.QUESTIONS["plan_to_move"]
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Asked: Plan to move to Morocco")
    state["current_question"] = "plan_to_move"
    return state


def question_preferred_cities(state: RecruiterState) -> RecruiterState:
    """
    Ask about preferred work cities.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with preferred cities question
    """
    msg = settings.QUESTIONS["preferred_cities"]
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Asked: Preferred work cities")
    state["current_question"] = "preferred_cities"
    return state


def question_call_center_experience(state: RecruiterState) -> RecruiterState:
    """
    Ask if candidate has call center experience.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with experience question
    """
    msg = settings.QUESTIONS["call_center_experience"]
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Asked: Call center experience")
    state["current_question"] = "call_center_experience"
    return state


def question_experience_details(state: RecruiterState) -> RecruiterState:
    """
    Ask for details about call center experience.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with experience details question
    """
    msg = settings.QUESTIONS["experience_details"]
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Asked: Experience details")
    state["current_question"] = "experience_details"
    return state


def question_why_call_center(state: RecruiterState) -> RecruiterState:
    """
    Ask why candidate thinks call center is right for them.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with motivation question
    """
    msg = settings.QUESTIONS["why_call_center"]
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Asked: Why call center")
    state["current_question"] = "why_call_center"
    return state


def question_salary_expectation(state: RecruiterState) -> RecruiterState:
    """
    Ask about salary expectation.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with salary question
    """
    msg = settings.QUESTIONS["salary_expectation"]
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Asked: Salary expectation")
    state["current_question"] = "salary_expectation"
    return state


def question_previous_applications(state: RecruiterState) -> RecruiterState:
    """
    Ask about previous call center applications.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with previous applications question
    """
    msg = settings.QUESTIONS["previous_applications"]
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Asked: Previous applications")
    state["current_question"] = "previous_applications"
    return state


def final_message(state: RecruiterState) -> RecruiterState:
    """
    Send final thank you message.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with final message
    """
    msg = settings.FINAL_MESSAGE
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Sent final thank you message")
    state["current_question"] = None
    return state