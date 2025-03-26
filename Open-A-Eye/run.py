"""
AI Companion - Main entry point

This script starts the AI Companion application.
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        logger.info("Starting AI Companion application")
        
        # Import the Flask app and config after environment variables are loaded
        from src.app import app
        from src.config.config import validate_config, HOST, PORT
        
        # Validate configuration
        validate_config()
        
        # Start the Flask application
        logger.info(f"Starting server on {HOST}:{PORT}")
        app.run(host=HOST, port=PORT, debug=True)
        
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        sys.exit(1) 