# 1. Install new dependencies
pip install -r requirements.txt

# 2. Update .env with Twilio credentials
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# 3. Start server
python scripts/run_server.py

# 4. In another terminal, start ngrok
ngrok http 5000

# 5. Configure Twilio webhook with ngrok URL
# https://your-ngrok-url.ngrok.io/webhook/whatsapp