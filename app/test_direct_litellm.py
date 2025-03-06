#!/usr/bin/env python3
"""
Test Direct LiteLLM Completion

This script tests the LiteLLM completion function directly.
"""

import os
import sys
import logging
from dotenv import load_dotenv
import litellm

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_litellm_completion():
    """Test the LiteLLM completion function directly."""
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
            
            # Set debug mode for more information
            os.environ["LITELLM_LOG"] = "DEBUG"
            
            # Set the API key directly in the environment
            os.environ["OPENAI_API_KEY"] = api_key
            
            # Create a simple test message
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, please respond with a simple 'Connection successful!' message."}
            ]
            
            try:
                logger.info("Calling LiteLLM completion function...")
                
                # Call LiteLLM with the API key explicitly passed
                response = litellm.completion(
                    model="gpt-3.5-turbo",  # Using a simpler model for testing
                    messages=messages,
                    temperature=0.7,
                    max_tokens=50,
                    api_key=api_key  # Explicitly pass the API key
                )
                
                # Extract and log the response
                response_text = response.choices[0].message.content
                logger.info(f"✅ LiteLLM connection successful! Response: {response_text}")
                return True
                
            except Exception as e:
                logger.error(f"❌ Error calling LiteLLM: {str(e)}")
                return False
        else:
            logger.error("LLM_API_KEY not found in environment variables!")
            return False
    else:
        logger.error(f".env file not found at: {env_path}")
        return False

if __name__ == "__main__":
    test_litellm_completion() 