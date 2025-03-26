import os
import csv
from datetime import datetime
from typing import List, Dict

class CSVDatabase:
    """Manages conversation storage in CSV format."""
    
    def __init__(self, csv_file: str = "conversations.csv"):
        self.csv_file = csv_file
        self._ensure_csv_exists()
    
    def _ensure_csv_exists(self) -> None:
        """Create CSV file if it doesn't exist."""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['user_phone', 'timestamp', 'role', 'content'])
    
    def get_conversation(self, user_phone: str) -> List[Dict[str, str]]:
        """Get conversation history for a user."""
        messages = []
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['user_phone'] == user_phone:
                        messages.append(row)
            return messages
        except Exception as e:
            print(f"Error reading conversation: {str(e)}")
            return []
    
    def add_message(self, user_phone: str, role: str, content: str) -> None:
        """Add a new message to the conversation."""
        try:
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    user_phone,
                    datetime.utcnow().isoformat(),
                    role,
                    content
                ])
        except Exception as e:
            print(f"Error adding message: {str(e)}")
    
    def get_conversation_history(self, user_phone: str, max_messages: int = 10) -> List[Dict[str, str]]:
        """Get formatted conversation history for OpenAI API."""
        messages = self.get_conversation(user_phone)
        
        # Sort by timestamp and get most recent messages
        messages.sort(key=lambda x: x['timestamp'])
        recent_messages = messages[-max_messages:] if len(messages) > max_messages else messages
        
        # Format for OpenAI API
        return [{"role": msg['role'], "content": msg['content']} for msg in recent_messages]


# Create a global instance for easy import
csv_db = CSVDatabase() 