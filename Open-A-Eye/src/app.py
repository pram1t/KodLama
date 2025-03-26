from flask import Flask, request
from src.config.config import validate_config
from src.twilio_handler import twilio_handler
app = Flask(__name__)

validate_config()

@app.route('/voice', methods=['POST'])
def voice():
    """Handle incoming voice calls."""
    # Get the caller's phone number
    caller_phone = request.values.get('From')
    
    # Handle the incoming call
    response = twilio_handler.handle_incoming_call(caller_phone)
    return response

@app.route('/handle-response', methods=['POST'])
def handle_response():
    """Handle user's spoken response."""
    # Get the caller's phone number and speech input
    caller_phone = request.values.get('From')
    user_input = request.values.get('SpeechResult', '')
    
    # Handle the user's response
    response = twilio_handler.handle_user_response(caller_phone, user_input)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 