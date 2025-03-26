import openai
from typing import List, Dict, Any, Optional

from src.config.config import OPENAI_API_KEY

# Configure OpenAI API key
openai.api_key = OPENAI_API_KEY


class AICompanion:
    """Manages interactions with the OpenAI API."""
    
    def __init__(self, model: str = "gpt-4", max_tokens: int = 150):
        self.model = model
        self.max_tokens = max_tokens
        self.system_message = (
            "You are a friendly and empathetic AI companion designed to help people feel less lonely. "
            "Engage in natural conversation, ask thoughtful questions, and remember details about the "
            "person you're talking with. Your goal is to make the user feel heard, understood, and valued."
        )
    
    def get_response(self, conversation_history: List[Dict[str, str]]) -> str:
        """
        Generate a response based on conversation history.
        
        Args:
            conversation_history: List of message dicts with 'role' and 'content'
        
        Returns:
            str: The AI's response
        """
        # Prepend system message to guide the AI's behavior
        messages = [{"role": "system", "content": self.system_message}]
        
        # Add conversation history
        messages.extend(conversation_history)
        
        # Generate response from OpenAI
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=0.7,  # Slightly creative but still focused
            n=1,
            stop=None
        )
        
        # Extract and return the response text
        return response.choices[0].message.content.strip()
    
    def customize_companion(self, personality: str, interests: List[str]) -> None:
        """
        Customize the AI companion's personality and interests.
        
        Args:
            personality: Description of the companion's personality
            interests: List of topics the companion should be knowledgeable about
        """
        interests_str = ", ".join(interests)
        
        self.system_message = (
            f"You are a friendly and empathetic AI companion with a {personality} personality. "
            f"You're knowledgeable about {interests_str}. "
            "Engage in natural conversation, ask thoughtful questions, and remember details about the "
            "person you're talking with. Your goal is to make the user feel heard, understood, and valued."
        )


# Create a global instance for easy import
ai_companion = AICompanion() 