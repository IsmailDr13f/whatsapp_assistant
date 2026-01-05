"""
Main entry point for the Recruiter Assistant.
"""
from src.models.state import RecruiterState
from src.graph.workflow import graph
from src.routers.flow_routers import meeting_router, permission_router, question_router
from src.nodes.meeting import meeting_unclear, send_booking_link
from src.nodes.permission import (
    permission_question,
    permission_unclear,
    persuasion_then_end,
    end_success
)
from src.nodes.questions import (
    question_location,
    question_city,
    question_plan_to_move,
    question_preferred_cities,
    question_call_center_experience,
    question_experience_details,
    question_why_call_center,
    question_salary_expectation,
    question_previous_applications,
    final_message
)


class RecruiterAssistant:
    """Main assistant class for managing conversation flow."""
    
    def __init__(self, first_name: str):
        """
        Initialize the assistant.
        
        Args:
            first_name: User's first name
        """
        self.state: RecruiterState = {
            "first_name": first_name,
            "meeting_booked": None,
            "permission_given": None,
            "messages": [],
            "log": [],
            "in_morocco": None,
            "current_city": None,
            "plan_to_move": None,
            "preferred_cities": None,
            "has_call_center_experience": None,
            "experience_details": None,
            "why_call_center": None,
            "salary_expectation": None,
            "previous_applications": None,
            "current_question": None
        }
        self.questions_started = False
    
    def start(self):
        """Start the conversation flow."""
        self.state = graph.invoke(self.state)
    
    def get_last_message(self) -> str:
        """Get the last assistant message."""
        if self.state["messages"]:
            return self.state["messages"][-1]["content"]
        return ""
    
    def get_new_messages(self, last_count: int) -> list:
        """Get new assistant messages since last check."""
        messages = []
        for msg in self.state["messages"][last_count:]:
            if msg["role"] == "assistant":
                messages.append(msg["content"])
        return messages
    
    def process_user_input(self, user_input: str) -> list:
        """
        Process user input and update conversation state.
        
        Args:
            user_input: User's response
            
        Returns:
            List of new assistant messages
        """
        # Track messages before processing
        message_count_before = len(self.state["messages"])
        
        self.state["messages"].append({"role": "user", "content": user_input})
        
        # Phase 1: Meeting booking
        if self.state["meeting_booked"] is None:
            route = meeting_router(self.state)
            
            if route == "meeting_unclear":
                self.state = meeting_unclear(self.state)
            elif route == "send_booking_link":
                self.state = send_booking_link(self.state)
                self.state = permission_question(self.state)
            elif route == "permission_question":
                self.state = permission_question(self.state)
        
        # Phase 2: Permission
        elif self.state["permission_given"] is None:
            route = permission_router(self.state)
            
            if route == "permission_unclear":
                self.state = permission_unclear(self.state)
            elif route == "persuasion_then_end":
                self.state = persuasion_then_end(self.state)
                # After persuasion, start questions anyway at the moment
                self.questions_started = True
                self.state = question_location(self.state)
            elif route == "end_success":
                self.state = end_success(self.state)
                self.questions_started = True
                self.state = question_location(self.state)
        
        # Phase 3: Questions
        elif self.questions_started and self.state["current_question"] is not None:
            route = question_router(self.state)
            
            # Execute the next question based on routing
            if route == "question_city":
                self.state = question_city(self.state)
            elif route == "question_plan_to_move":
                self.state = question_plan_to_move(self.state)
            elif route == "question_preferred_cities":
                self.state = question_preferred_cities(self.state)
            elif route == "question_call_center_experience":
                self.state = question_call_center_experience(self.state)
            elif route == "question_experience_details":
                self.state = question_experience_details(self.state)
            elif route == "question_why_call_center":
                self.state = question_why_call_center(self.state)
            elif route == "question_salary_expectation":
                self.state = question_salary_expectation(self.state)
            elif route == "question_previous_applications":
                self.state = question_previous_applications(self.state)
            elif route == "final_message":
                self.state = final_message(self.state)
        
        # Return new assistant messages
        return self.get_new_messages(message_count_before)
    
    def is_completed(self) -> bool:
        """Check if conversation is completed."""
        return (
            self.state["current_question"] is None and 
            self.questions_started and
            self.state["permission_given"] is not None
        )
    
    def get_state(self) -> RecruiterState:
        """Get current state."""
        return self.state
    
    def get_collected_data(self) -> dict:
        """Get all collected candidate data."""
        return {
            "first_name": self.state["first_name"],
            "meeting_booked": self.state["meeting_booked"],
            "permission_given": self.state["permission_given"],
            "in_morocco": self.state["in_morocco"],
            "current_city": self.state["current_city"],
            "plan_to_move": self.state["plan_to_move"],
            "preferred_cities": self.state["preferred_cities"],
            "has_call_center_experience": self.state["has_call_center_experience"],
            "experience_details": self.state["experience_details"],
            "why_call_center": self.state["why_call_center"],
            "salary_expectation": self.state["salary_expectation"],
            "previous_applications": self.state["previous_applications"]
        }