"""
Webhook handlers for processing incoming WhatsApp messages.
"""
from typing import List
from src.services.session_manager import session_manager
from src.services.twilio_service import twilio_service


def handle_whatsapp_message(from_number: str, message: str, profile_name: str) -> List[str]:
    """
    Handle incoming WhatsApp message and generate response.
    
    Args:
        from_number: Sender's WhatsApp number
        message: Message content
        profile_name: Sender's profile name
        
    Returns:
        List of response messages
    """
    # Handle special commands
    if message.lower() in ['reset', 'restart', 'start over']:
        session_manager.delete_session(from_number)
        assistant = session_manager.get_or_create_session(from_number, profile_name)
        return [assistant.get_last_message()]
    
    if message.lower() in ['help', 'info']:
        return [
            "I'm the Linkrs Marokko recruitment assistant. I'll help you prepare for your interview by asking a few questions.\n\n"
            "Commands:\n"
            "- Type 'reset' to start over\n"
            "- Type 'status' to see your progress"
        ]
    
    if message.lower() == 'status':
        assistant = session_manager.get_session(from_number)
        if assistant:
            data = assistant.get_collected_data()
            status = "✅ Completed" if assistant.is_completed() else "📝 In Progress"
            return [
                f"Status: {status}\n"
                f"Meeting booked: {data.get('meeting_booked', 'Not answered')}\n"
                f"Questions answered: {sum(1 for v in data.values() if v is not None)}"
            ]
        else:
            return ["No active session. Send any message to start!"]
    
    # Get or create session
    assistant = session_manager.get_or_create_session(from_number, profile_name)
    
    # Check if this is the first message (welcome message not sent yet)
    if len(assistant.state["messages"]) == 1:
        # This is a new session, return welcome message
        return [assistant.get_last_message()]
    
    # Process user input
    response_messages = assistant.process_user_input(message)
    
    # If we got multiple messages, send additional ones via Twilio API
    if len(response_messages) > 1:
        # Send additional messages (skip the first one as it will be returned)
        for msg in response_messages[1:]:
            twilio_service.send_message(from_number, msg)
    
    # Return the first message (or empty list if no messages)
    return response_messages[:1] if response_messages else ["Thank you for your message."]


def handle_status_callback(message_sid: str, message_status: str):
    """
    Handle Twilio message status callbacks.
    
    Args:
        message_sid: Message SID
        message_status: Status (sent, delivered, failed, etc.)
    """
    print(f"Message {message_sid} status: {message_status}")
    
    # You can implement logging or tracking here
    if message_status == "failed":
        print(f"Message {message_sid} failed to deliver")
    elif message_status == "delivered":
        print(f"Message {message_sid} delivered successfully")