"""
Routing logic for conversation flow.
"""
from typing import Literal
from src.models.state import RecruiterState
from src.services.llm_service import llm_service


MeetingRoute = Literal["meeting_unclear", "permission_question", "send_booking_link"]
PermissionRoute = Literal["permission_unclear", "end_success", "persuasion_then_end"]
QuestionRoute = Literal[
    "question_city",
    "question_plan_to_move",
    "question_preferred_cities",
    "question_call_center_experience",
    "question_experience_details",
    "question_why_call_center",
    "question_salary_expectation",
    "question_previous_applications",
    "final_message"
]


def meeting_router(state: RecruiterState) -> MeetingRoute:
    """
    Route based on meeting booking response.
    
    Args:
        state: Current conversation state
        
    Returns:
        Next node to execute
    """
    last_user_msg = state["messages"][-1]["content"]
    answer = llm_service.classify_yes_no(last_user_msg)
    
    if answer is None:
        return "meeting_unclear"
    
    state["meeting_booked"] = answer
    
    if answer:
        return "permission_question"
    else:
        return "send_booking_link"


def permission_router(state: RecruiterState) -> PermissionRoute:
    """
    Route based on permission response.
    
    Args:
        state: Current conversation state
        
    Returns:
        Next node to execute
    """
    last_user_msg = state["messages"][-1]["content"]
    answer = llm_service.classify_yes_no(last_user_msg)
    
    if answer is None:
        return "permission_unclear"
    
    state["permission_given"] = answer
    
    if answer:
        return "end_success"
    else:
        return "persuasion_then_end"


def question_router(state: RecruiterState) -> QuestionRoute:
    """
    Route to next question based on current question and answer.
    
    Args:
        state: Current conversation state
        
    Returns:
        Next question node to execute
    """
    current = state.get("current_question")
    last_user_msg = state["messages"][-1]["content"]
    
    if current == "location":
        # Store the answer
        answer = llm_service.classify_yes_no(last_user_msg)
        state["in_morocco"] = answer
        
        if answer:
            return "question_city"
        else:
            return "question_plan_to_move"
    
    elif current == "city":
        state["current_city"] = last_user_msg
        return "question_preferred_cities"
    
    elif current == "plan_to_move":
        state["plan_to_move"] = last_user_msg
        return "question_preferred_cities"
    
    elif current == "preferred_cities":
        state["preferred_cities"] = last_user_msg
        return "question_call_center_experience"
    
    elif current == "call_center_experience":
        answer = llm_service.classify_yes_no(last_user_msg)
        state["has_call_center_experience"] = answer
        
        if answer:
            return "question_experience_details"
        else:
            return "question_why_call_center"
    
    elif current == "experience_details":
        state["experience_details"] = last_user_msg
        return "question_salary_expectation"
    
    elif current == "why_call_center":
        state["why_call_center"] = last_user_msg
        return "question_salary_expectation"
    
    elif current == "salary_expectation":
        state["salary_expectation"] = last_user_msg
        return "question_previous_applications"
    
    elif current == "previous_applications":
        state["previous_applications"] = last_user_msg
        return "final_message"
    
    # Default to first question
    return "question_preferred_cities"