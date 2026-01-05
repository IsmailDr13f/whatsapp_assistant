"""
Script to initiate a conversation with a candidate via WhatsApp.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.twilio_service import twilio_service
from src.services.session_manager import session_manager
from config.settings import settings


def validate_phone_number(phone: str) -> str:
    """
    Validate and format phone number for Twilio WhatsApp.
    Returns: 'whatsapp:+<E164>'
    """
    phone = phone.strip()
    phone = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

    # remove whatsapp: if user pasted it already
    if phone.startswith("whatsapp:"):
        phone = phone[len("whatsapp:"):]

    if not phone.startswith("+"):
        phone = "+" + phone

    return f"whatsapp:{phone}"


def initiate_conversation(first_name: str, phone_number: str, restart: bool = False) -> dict:
    """
    Proactively send the welcome message to a candidate.

    Args:
        first_name: Candidate first name
        phone_number: Candidate phone in E.164 (+...) or local (will be normalized)
        restart: If True, delete any existing session and start fresh

    Returns:
        Dict with success/error + details
    """
    # Validate configuration
    try:
        settings.validate()
    except ValueError as e:
        return {"success": False, "error": f"Configuration error: {e}"}

    formatted_phone = validate_phone_number(phone_number)

    # Optionally restart session (useful for testing)
    if restart:
        session_manager.delete_session(formatted_phone)

    # Create or get session
    assistant = session_manager.get_or_create_session(formatted_phone, first_name)

    # Safety: if for any reason the assistant hasn't produced messages yet, start it.
    if not assistant.state.get("messages"):
        assistant.start()

    # Welcome message (last assistant message from start flow)
    welcome_message = assistant.get_last_message() or "Hi! 👋"

    # Send message via Twilio
    result = twilio_service.send_message(formatted_phone, welcome_message)

    if result.get("success"):
        return {
            "success": True,
            "phone_number": formatted_phone,
            "ProfileName": first_name,
            "message_sid": result.get("sid"),
            "status": result.get("status"),
            "message_sent": welcome_message,
        }

    return {
        "success": False,
        "phone_number": formatted_phone,
        "error": result.get("error", "Failed to send message"),
    }


def main():
    """
    CLI usage:
      python initiate_conversation.py
    """
    print("\n" + "=" * 60)
    print("This Information should be provided in the applying process in our website:")
    print("=" * 60 + "\n")

    first_name = input("Enter candidate's first name: ").strip()
    if not first_name:
        print("❌ First name is required!")
        return

    phone_number = input("Enter candidate's WhatsApp number (with country code): ").strip()
    if not phone_number:
        print("❌ Phone number is required!")
        return

    restart_choice = input("Restart session if it already exists? (yes/no): ").strip().lower()
    restart = restart_choice in ["yes", "y", "oui", "o"]

    result = initiate_conversation(first_name, phone_number, restart=restart)

    if result["success"]:
        print("\n✅ Message sent successfully!")
        print(f"   To: {result['phone_number']}")
        print(f"   SID: {result.get('message_sid')}")
        print(f"   Status: {result.get('status')}")
        print(f"\n📝 Sent:\n{result.get('message_sent')}\n")
    else:
        print("\n❌ Failed to initiate conversation.")
        print(f"   To: {result.get('phone_number')}")
        print(f"   Error: {result.get('error')}")


if __name__ == "__main__":
    main()
