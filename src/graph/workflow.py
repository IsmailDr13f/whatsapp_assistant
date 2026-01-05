"""
LangGraph workflow construction.
"""
from langgraph.graph import StateGraph
from src.models.state import RecruiterState
from src.nodes.welcome import welcome_and_meeting_question
from src.nodes.meeting import meeting_unclear, send_booking_link
from src.nodes.permission import (
    permission_question,
    permission_unclear,
    persuasion_then_end,
    end_success
)


def build_workflow() -> StateGraph:
    """
    Build and compile the conversation workflow graph.
    
    Returns:
        Compiled StateGraph
    """
    builder = StateGraph(RecruiterState)
    
    # Add all nodes
    builder.add_node("welcome_and_meeting_question", welcome_and_meeting_question)
    builder.add_node("meeting_unclear", meeting_unclear)
    builder.add_node("send_booking_link", send_booking_link)
    builder.add_node("permission_question", permission_question)
    builder.add_node("permission_unclear", permission_unclear)
    builder.add_node("persuasion_then_end", persuasion_then_end)
    builder.add_node("end_success", end_success)
    
    # Set entry point
    builder.set_entry_point("welcome_and_meeting_question")
    
    # Compile and return
    return builder.compile()


# Global graph instance
graph = build_workflow()