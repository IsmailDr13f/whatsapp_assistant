"""
Flask application for Twilio WhatsApp webhook.
"""
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from config.settings import settings
from src.api.webhooks import handle_whatsapp_message


def create_app():
    """
    Create and configure Flask application.
    
    Returns:
        Configured Flask app
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = settings.FLASK_SECRET_KEY
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            "status": "healthy",
            "service": "recruiter-assistant-whatsapp"
        }), 200
    
    @app.route('/webhook/whatsapp', methods=['POST'])
    def whatsapp_webhook():
        """
        Twilio WhatsApp webhook endpoint.
        Receives incoming messages from WhatsApp users.
        """
        try:
            # Get incoming message data
            incoming_msg = request.form.get('Body', '').strip()
            from_number = request.form.get('From', '')
            profile_name = request.form.get('ProfileName', 'User')
            
            print(f"Received message from {from_number} / Name: ({profile_name}) / Message: {incoming_msg}")
            
            # Handle the message and get response
            response_messages = handle_whatsapp_message(
                from_number=from_number,
                message=incoming_msg,
                profile_name=profile_name
            )
            
            # Create Twilio response (only for the first message, others sent via API)
            resp = MessagingResponse()
            if response_messages:
                resp.message(response_messages[0])
            
            return str(resp), 200
        
        except Exception as e:
            print(f"Error in webhook: {e}")
            resp = MessagingResponse()
            resp.message("Sorry, I encountered an error. Please try again.")
            return str(resp), 500
    
    @app.route('/session/<phone_number>', methods=['GET'])
    def get_session_info(phone_number):
        """
        Get information about a user's session.
        For debugging and monitoring purposes.
        """
        from src.services.session_manager import session_manager
        
        # Add whatsapp: prefix if not present
        if not phone_number.startswith('whatsapp:'):
            phone_number = f'whatsapp:{phone_number}'
        
        info = session_manager.get_session_info(phone_number)
        
        if info:
            return jsonify({
                "success": True,
                "session": {
                    "phone_number": info["phone_number"],
                    "created_at": info["created_at"].isoformat(),
                    "last_activity": info["last_activity"].isoformat(),
                    "is_completed": info["is_completed"],
                    "collected_data": info["collected_data"]
                }
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "Session not found"
            }), 404
    
    @app.route('/sessions', methods=['GET'])
    def get_all_sessions():
        """Get count of active sessions."""
        from src.services.session_manager import session_manager
        
        return jsonify({
            "active_sessions": session_manager.get_active_sessions_count()
        }), 200
    
    @app.errorhandler(404)
    def not_found(e):
        """Handle 404 errors."""
        return jsonify({"error": "Endpoint not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        """Handle 500 errors."""
        return jsonify({"error": "Internal server error"}), 500

    @app.route('/', methods=['POST'])
    def root_webhook():
        # Twilio is currently POSTing to '/'
        return whatsapp_webhook()

    
    return app