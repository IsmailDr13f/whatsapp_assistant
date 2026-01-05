"""
Welcome and initial meeting question node.
"""
from config.settings import settings
from src.models.state import RecruiterState


def welcome_and_meeting_question(state: RecruiterState) -> RecruiterState:
    """
    Send welcome message and ask about meeting booking.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with welcome message
    """
    msg = settings.WELCOME_MESSAGE_TEMPLATE.format(
        first_name=state['first_name']
    )
    
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Sent welcome + meeting question")
    
    return state