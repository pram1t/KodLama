from twilio.twiml.voice_response import VoiceResponse, Gather
from typing import Optional

from src.database.csv_db import csv_db
from src.ai.openai_client import ai_companion


class TwilioHandler:
    """Handles Twilio voice interactions."""
    
    def __init__(self):
        self.welcome_message = "Hello! I'm your AI companion. How are you feeling today?"
    
    def handle_incoming_call(self, caller_phone: str) -> str:
        """
        Handle an incoming call and generate TwiML response.
        
        Args:
            caller_phone: The phone number of the caller
            
        Returns:
            str: TwiML response as a string
        """
        # Create TwiML response
        resp = VoiceResponse()
        
        # Check if this is a returning caller
        conversation = csv_db.get_conversation(caller_phone)
        
        if conversation:
            # Returning caller - personalized greeting
            message = "Welcome back! It's good to hear from you again. How have you been since we last talked?"
        else:
            # New caller - standard greeting
            message = self.welcome_message
        
        # Store assistant's greeting in conversation history
        csv_db.add_message(caller_phone, "assistant", message)
        
        # Add greeting and gather user input
        gather = Gather(
            input='speech',
            action='/handle-response',
            method='POST',
            speech_timeout='auto',
            language='en-US',
            enhanced=True  # Enable enhanced speech recognition
        )
        gather.say(message, voice='Polly.Amy')  # Use a more natural voice
        
        # Add the gather to the response
        resp.append(gather)
        
        # If no input is received, end the call gracefully
        resp.say("I didn't catch that. Feel free to call back anytime. Goodbye!")
        resp.hangup()
        
        return str(resp)
    
    def handle_user_response(self, caller_phone: str, user_input: str) -> str:
        """
        Process user's spoken response and generate AI reply.
        
        Args:
            caller_phone: The phone number of the caller
            user_input: The transcribed text of the user's speech
            
        Returns:
            str: TwiML response as a string
        """
        # Store user's message in conversation history
        csv_db.add_message(caller_phone, "user", user_input)
        
        # Get conversation history
        conversation_history = csv_db.get_conversation_history(caller_phone)
        
        # Generate AI response based on conversation history
        ai_response = ai_companion.get_response(conversation_history)
        
        # Store AI's response in conversation history
        csv_db.add_message(caller_phone, "assistant", ai_response)
        
        # Create TwiML response with AI's message
        resp = VoiceResponse()
        
        # Add AI response and gather next user input
        gather = Gather(
            input='speech',
            action='/handle-response',
            method='POST',
            speech_timeout='auto',
            language='en-US',
            enhanced=True  # Enable enhanced speech recognition
        )
        gather.say(ai_response, voice='Polly.Amy')  # Use a more natural voice
        
        # Add the gather to the response
        resp.append(gather)
        
        # If no input is received, end the call gracefully
        resp.say("I didn't catch that. Thank you for talking with me today. Feel free to call back anytime. Goodbye!")
        resp.hangup()
        
        return str(resp)


# Create a global instance for easy import
twilio_handler = TwilioHandler() 