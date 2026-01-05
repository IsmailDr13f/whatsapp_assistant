"""
Run the Flask server for WhatsApp integration.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api.app import create_app
from config.settings import settings


def main():
    """Run the Flask application."""
    # Validate settings
    try:
        settings.validate()
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\nPlease ensure the following environment variables are set:")
        print("  - DEEPINFRA_API_KEY")
        print("  - TWILIO_ACCOUNT_SID")
        print("  - TWILIO_AUTH_TOKEN")
        print("  - TWILIO_WHATSAPP_NUMBER (optional, defaults to sandbox)")
        return
    
    print("=" * 60)
    print("🚀 Starting Recruiter Assistant WhatsApp Server")
    print("=" * 60)
    print(f"\n📱 WhatsApp Number: {settings.TWILIO_WHATSAPP_NUMBER}")
    print(f"🌐 Host: {settings.FLASK_HOST}")
    print(f"🔌 Port: {settings.FLASK_PORT}")
    print(f"🐛 Debug: {settings.FLASK_DEBUG}")
    print("\n📍 Endpoints:")
    print(f"  - Health Check: http://{settings.FLASK_HOST}:{settings.FLASK_PORT}/health")
    print(f"  - WhatsApp Webhook: http://{settings.FLASK_HOST}:{settings.FLASK_PORT}/webhook/whatsapp")
    print(f"  - Sessions: http://{settings.FLASK_HOST}:{settings.FLASK_PORT}/sessions")
    print("\n" + "=" * 60)
    print("✅ Server is ready to receive WhatsApp messages!")
    print("=" * 60 + "\n")
    
    # Create and run app
    app = create_app()
    app.run(
        host=settings.FLASK_HOST,
        port=settings.FLASK_PORT,
        debug=settings.FLASK_DEBUG
    )


if __name__ == "__main__":
    main()

