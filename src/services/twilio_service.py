"""
Twilio service for sending WhatsApp messages.
"""
from twilio.rest import Client
from config.settings import settings


class TwilioService:
    """Service for sending WhatsApp messages via Twilio."""
    
    def __init__(self):
        """Initialize Twilio client."""
        self.client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )
        self.from_number = settings.TWILIO_WHATSAPP_NUMBER
    
    def send_message(self, to_number: str, message: str) -> dict:
        """
        Send a WhatsApp message to a user.
        
        Args:
            to_number: Recipient's WhatsApp number (format: whatsapp:+1234567890)
            message: Message content to send
            
        Returns:
            Dictionary with message SID and status
        """
        try:
            # Ensure number has whatsapp: prefix
            if not to_number.startswith("whatsapp:"):
                to_number = f"whatsapp:{to_number}"
            
            message_obj = self.client.messages.create(
                from_=self.from_number,
                body=message,
                to=to_number
            )
            
            return {
                "success": True,
                "sid": message_obj.sid,
                "status": message_obj.status
            }
        
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def send_multiple_messages(self, to_number: str, messages: list) -> list:
        """
        Send multiple messages to a user.
        
        Args:
            to_number: Recipient's WhatsApp number
            messages: List of message contents
            
        Returns:
            List of results for each message
        """
        results = []
        for message in messages:
            result = self.send_message(to_number, message)
            results.append(result)
        return results


# Global instance
twilio_service = TwilioService()