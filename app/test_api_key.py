#!/usr/bin/env python3
"""
Test API Key Loading

This script tests the loading of the API key from the .env file.
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_api_key_loading():
    """Test the loading of the API key from the .env file."""
    # Get the absolute path to the .env file
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    logger.info(f"Looking for .env file at: {env_path}")
    
    # Check if the .env file exists
    if os.path.exists(env_path):
        logger.info(f".env file found at: {env_path}")
        
        # Load the .env file
        load_dotenv(env_path)
        logger.info("Loaded .env file")
        
        # Get the API key
        api_key = os.getenv("LLM_API_KEY")
        
        # Check if the API key is set
        if api_key:
            # Mask the API key for security
            masked_key = api_key[:5] + "..." + api_key[-4:] if len(api_key) > 10 else "***"
            logger.info(f"API key loaded: {masked_key}")
            
            # Check if the API key starts with "sk-"
            if api_key.startswith("sk-"):
                logger.info("API key format appears valid (starts with 'sk-')")
            else:
                logger.warning("API key format may be invalid (does not start with 'sk-')")
            
            # Check if the API key is long enough
            if len(api_key) > 20:
                logger.info("API key length appears valid")
            else:
                logger.warning("API key length may be too short")
                
            # Print the environment variables
            logger.info("Environment variables:")
            for key, value in os.environ.items():
                if "API_KEY" in key or "LLM" in key:
                    masked_value = value[:5] + "..." + value[-4:] if len(value) > 10 else "***"
                    logger.info(f"  {key}: {masked_value}")
        else:
            logger.error("LLM_API_KEY not found in environment variables!")
    else:
        logger.error(f".env file not found at: {env_path}")

if __name__ == "__main__":
    test_api_key_loading() 