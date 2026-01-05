"""
LLM service for intent classification and text generation.
"""
import json
from typing import Optional
from langchain_openai import ChatOpenAI
from config.settings import settings
from src.models.state import YesNoIntent


class LLMService:
    """Service for interacting with the LLM."""
    
    def __init__(self):
        """Initialize the LLM client."""
        self.llm = ChatOpenAI(
            model=settings.MODEL_NAME,
            api_key=settings.DEEPINFRA_API_KEY,
            base_url=settings.DEEPINFRA_BASE_URL,
            temperature=settings.TEMPERATURE
        )
    
    def classify_yes_no(self, user_text: str) -> Optional[bool]:
        """
        Classify user response as yes/no/unclear.
        
        Args:
            user_text: The user's response text
            
        Returns:
            True for yes, False for no, None for unclear
        """
        prompt = f"""
You are a classifier. The user responded to a yes/no question.

Return ONLY JSON in this schema:
{{
  "answer": true/false/null,
  "confidence": 0.0-1.0,
  "reasoning": "short explanation"
}}

User response: "{user_text}"
"""
        
        try:
            res = self.llm.invoke(prompt)
            data = json.loads(res.content)
            parsed = YesNoIntent(**data)
            
            # Only accept when confidence is high enough
            if parsed.confidence < settings.CONFIDENCE_THRESHOLD:
                return None
            
            return parsed.answer
        
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing LLM response: {e}")
            return None


# Global instance
llm_service = LLMService()