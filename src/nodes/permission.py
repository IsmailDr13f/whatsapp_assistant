"""
Permission-related conversation nodes.
"""
from src.models.state import RecruiterState


def permission_question(state: RecruiterState) -> RecruiterState:
    """
    Ask for permission to continue with questions.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with permission question
    """
    msg = "Is it okay if we ask you a couple of questions to prepare ourselves for the upcoming meeting?"
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Asked permission")
    return state


def permission_unclear(state: RecruiterState) -> RecruiterState:
    """
    Handle unclear response to permission question.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state asking for clarification
    """
    msg = "Just to confirm — is it okay if we ask you a few questions? (yes/no)"
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Permission unclear → asked again")
    return state


def persuasion_then_end(state: RecruiterState) -> RecruiterState:
    """
    Send persuasion message when permission is denied.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with persuasion message
    """
    msg = (
        "No worries — these questions help our recruiter prepare and make the meeting more effective. "
        "It takes only about 2 minutes."
    )
    state["messages"].append({"role": "assistant", "content": msg})
    state["log"].append("Permission denied → persuasion sent")
    return state


def end_success(state: RecruiterState) -> RecruiterState:
    """
    Permission granted - move to first question.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state (questions will continue in main loop)
    """
    state["log"].append("Permission granted - starting questions")
    return state