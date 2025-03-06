#!/usr/bin/env python3
"""
Test LLM Connection Script

This script tests the connection to the LLM provider using LiteLLM.
It loads the API key from the .env file and sends a simple test message.
"""

import os
import sys
import logging
from dotenv import load_dotenv
import litellm

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_llm_connection():
    """Test the connection to the LLM provider."""
    # Load environment variables
    load_dotenv()
    
    # Get LLM configuration from environment variables
    api_key = os.getenv("LLM_API_KEY")
    provider = os.getenv("LLM_PROVIDER", "openai")
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    
    if not api_key:
        logger.error("❌ LLM_API_KEY not found in environment variables!")
        return False
    
    # Check if the API key looks valid
    if api_key.startswith("sk-") and len(api_key) > 20:
        logger.info(f"API key format looks valid (starts with 'sk-' and has sufficient length)")
    else:
        logger.warning(f"API key format may be invalid. Should start with 'sk-' and be longer than 20 characters.")
    
    logger.info(f"Testing LLM connection with provider: {provider}, model: {model}")
    
    # Create a simple test message
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, please respond with a simple 'Connection successful!' message."}
    ]
    
    try:
        # Enable debug mode for more detailed error information
        litellm.set_verbose = True
        
        # Call LiteLLM with the API key explicitly passed
        response = litellm.completion(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=50,
            api_key=api_key
        )
        
        # Extract and log the response
        response_text = response.choices[0].message.content
        logger.info(f"✅ LLM connection successful! Response: {response_text}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error connecting to LLM: {str(e)}")
        
        # Provide more detailed troubleshooting information
        logger.info("\nTroubleshooting tips:")
        logger.info("1. Check if your API key is valid and has not expired")
        logger.info("2. Verify that you have sufficient credits in your account")
        logger.info("3. Confirm that the model 'gpt-4o-mini' is available for your account")
        logger.info("4. Check if there are any outages reported for the OpenAI API")
        logger.info("5. Try using a different model like 'gpt-3.5-turbo'")
        
        return False

if __name__ == "__main__":
    # Run the test
    success = test_llm_connection()
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1) 