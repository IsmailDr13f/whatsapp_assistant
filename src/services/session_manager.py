"""
Session manager for handling multiple user conversations.
"""
from typing import Dict, Optional
from datetime import datetime, timedelta
from src.main import RecruiterAssistant
from config.settings import settings


class SessionManager:
    """Manage conversation sessions for multiple users."""
    
    def __init__(self):
        """Initialize session storage."""
        self.sessions: Dict[str, dict] = {}
    
    def get_or_create_session(self, phone_number: str, first_name: str = None) -> RecruiterAssistant:
        """
        Get existing session or create new one.
        
        Args:
            phone_number: User's phone number (session key)
            first_name: User's first name (for new sessions)
            
        Returns:
            RecruiterAssistant instance
        """
        # Clean up expired sessions
        self._cleanup_expired_sessions()
        
        # Check if session exists
        if phone_number in self.sessions:
            session_data = self.sessions[phone_number]
            session_data["last_activity"] = datetime.now()
            return session_data["assistant"]
        
        # Create new session
        assistant = RecruiterAssistant(first_name or "there")
        assistant.start()
        
        self.sessions[phone_number] = {
            "assistant": assistant,
            "created_at": datetime.now(),
            "last_activity": datetime.now(),
            "phone_number": phone_number
        }
        
        return assistant
    
    def get_session(self, phone_number: str) -> Optional[RecruiterAssistant]:
        """
        Get existing session without creating new one.
        
        Args:
            phone_number: User's phone number
            
        Returns:
            RecruiterAssistant instance or None
        """
        if phone_number in self.sessions:
            return self.sessions[phone_number]["assistant"]
        return None
    
    def delete_session(self, phone_number: str):
        """
        Delete a user's session.
        
        Args:
            phone_number: User's phone number
        """
        if phone_number in self.sessions:
            del self.sessions[phone_number]
    
    def _cleanup_expired_sessions(self):
        """Remove sessions that have been inactive for too long."""
        now = datetime.now()
        timeout = timedelta(minutes=settings.SESSION_TIMEOUT_MINUTES)
        
        expired_sessions = [
            phone for phone, data in self.sessions.items()
            if now - data["last_activity"] > timeout
        ]
        
        for phone in expired_sessions:
            print(f"Cleaning up expired session for {phone}")
            del self.sessions[phone]
    
    def get_active_sessions_count(self) -> int:
        """Get count of active sessions."""
        return len(self.sessions)
    
    def get_session_info(self, phone_number: str) -> Optional[dict]:
        """
        Get session information.
        
        Args:
            phone_number: User's phone number
            
        Returns:
            Session info dictionary or None
        """
        if phone_number in self.sessions:
            data = self.sessions[phone_number]
            assistant = data["assistant"]
            
            return {
                "phone_number": phone_number,
                "created_at": data["created_at"],
                "last_activity": data["last_activity"],
                "is_completed": assistant.is_completed(),
                "collected_data": assistant.get_collected_data()
            }
        return None
    
    def is_new_session(self, phone_number: str) -> bool:
        """
        Check if this is the very first interaction for a user session.
        
        Returns:
            True if session was just created and welcome message hasn't been sent
        """
        if phone_number not in self.sessions:
            return False
        
        session_data = self.sessions[phone_number]
        # Check if assistant has only the initial welcome message (no user responses yet)
        return len(session_data["assistant"].state.get("messages", [])) <= 1


# Global instance
session_manager = SessionManager()