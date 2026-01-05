"""
Meeting-related conversation nodes.
"""
from config.settings import settings
from src.models.state import RecruiterState


def meeting_unclear(state: RecruiterState) -> RecruiterState:
    """
    Handle unclear response to meeting question.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state asking for clarification
    """
    msg = "Sorry, I didn't fully catch that — have you already booked a meeting? (yes/no)"
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Meeting unclear → asked again")
    return state


def send_booking_link(state: RecruiterState) -> RecruiterState:
    """
    Send booking link when user hasn't booked a meeting.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with booking link
    """
    msg = (
        "No problem! Please book a meeting using this link:\n"
        f"{settings.BOOKING_LINK}\n\n"
        "After booking, I'll ask you a couple of quick questions to prepare for the meeting."
    )
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Meeting not booked → sent link")
    return state