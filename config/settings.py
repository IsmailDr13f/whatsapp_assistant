"""
Configuration settings for the Recruiter Assistant.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings and configuration."""
    
    # API Configuration
    DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")
    DEEPINFRA_BASE_URL = "https://api.deepinfra.com/v1/openai"
    MODEL_NAME = "openai/gpt-oss-120b"
    
    # LLM Parameters
    TEMPERATURE = 0.5
    CONFIDENCE_THRESHOLD = 0.65
    
    # Twilio Configuration
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")
    
    # Flask Configuration
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")
    FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    # Session Configuration
    SESSION_TIMEOUT_MINUTES = 60
    
    # URLs
    BOOKING_LINK = "https://linkrsmarokko.com/book-meeting"
    
    # Messages
    WELCOME_MESSAGE_TEMPLATE = (
        "Thank you {first_name} for your application via the Linkrsmarokko website. "
        "Have you been able to book a meeting via the website with one of our recruiters?"
    )
    
    # Question Messages
    QUESTIONS = {
        "location": "Are you currently in Morocco?",
        "city": "In what city are you currently residing?",
        "plan_to_move": "How concrete is your plan to come to Morocco? When are you planning to come and live in Morocco?",
        "preferred_cities": "Which cities would you prefer to work in?",
        "call_center_experience": "Do you already have experience working in call centers?",
        "experience_details": "Can you tell me about your call center experiences, what tasks you performed, and the dates you worked?",
        "why_call_center": "Why do you think working in a call center is the right job for you?",
        "salary_expectation": "What is your salary expectation?",
        "previous_applications": "Which call centers have you already applied to in Morocco?",
    }
    
    FINAL_MESSAGE = (
        "Thank you for answering our questions. Please let us know if you have any additional questions. "
        "Otherwise, we look forward to meeting you."
    )
    
    @classmethod
    def validate(cls):
        """Validate required settings."""
        if not cls.DEEPINFRA_API_KEY:
            raise ValueError("DEEPINFRA_API_KEY is not set in environment variables")
        if not cls.TWILIO_ACCOUNT_SID:
            raise ValueError("TWILIO_ACCOUNT_SID is not set in environment variables")
        if not cls.TWILIO_AUTH_TOKEN:
            raise ValueError("TWILIO_AUTH_TOKEN is not set in environment variables")


settings = Settings()