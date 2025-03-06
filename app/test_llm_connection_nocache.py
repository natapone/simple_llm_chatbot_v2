#!/usr/bin/env python3
"""
No-Cache Test LLM Connection Script

This script tests the connection to the LLM provider using LiteLLM.
It explicitly reloads environment variables and clears any potential caches.
"""

import os
import sys
import logging
import importlib
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_llm_connection():
    """Test the connection to the LLM provider with cache clearing."""
    # Force reload of environment variables
    if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')):
        logger.info("Loading environment variables from .env file")
        load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'), override=True)
    else:
        logger.warning(".env file not found in the expected location")
    
    # Get LLM configuration from environment variables
    api_key = os.getenv("LLM_API_KEY")
    provider = os.getenv("LLM_PROVIDER", "openai")
    model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")  # Using gpt-3.5-turbo for testing
    
    if not api_key:
        logger.error("❌ LLM_API_KEY not found in environment variables!")
        return False
    
    # Log the API key format (safely)
    masked_key = api_key[:5] + "..." + api_key[-4:] if len(api_key) > 10 else "***"
    logger.info(f"Using API key: {masked_key}")
    
    # Set environment variables directly
    os.environ["LITELLM_API_KEY"] = api_key
    os.environ["OPENAI_API_KEY"] = api_key
    
    # Try a direct OpenAI API call first
    try:
        logger.info("Attempting direct OpenAI API call...")
        import openai
        openai.api_key = api_key
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, please respond with a simple 'Connection successful!' message."}
            ],
            temperature=0.7,
            max_tokens=50
        )
        
        response_text = response.choices[0].message.content
        logger.info(f"✅ OpenAI API connection successful! Response: {response_text}")
        
        # If OpenAI direct call works, try LiteLLM
        logger.info("Now testing with LiteLLM...")
        
        # Import litellm after setting environment variables
        import litellm
        
        # Set debug mode for more information
        os.environ["LITELLM_LOG"] = "DEBUG"
        
        logger.info(f"Testing LiteLLM connection with provider: {provider}, model: {model}")
        
        # Create a simple test message
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, please respond with a simple 'Connection successful!' message."}
        ]
        
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
        logger.info(f"✅ LiteLLM connection successful! Response: {response_text}")
        return True
        
    except ImportError as e:
        logger.error(f"❌ Error importing OpenAI or LiteLLM: {str(e)}")
        logger.info("Make sure you have the required packages installed:")
        logger.info("pip install openai litellm")
        return False
        
    except Exception as e:
        logger.error(f"❌ Error connecting to LLM: {str(e)}")
        
        # Provide more detailed troubleshooting information
        logger.info("\nTroubleshooting tips:")
        logger.info("1. Verify the API key in your .env file is correct and up-to-date")
        logger.info("2. Check if your OpenAI account has sufficient credits")
        logger.info("3. Try using a different model like 'gpt-3.5-turbo'")
        logger.info("4. Check your internet connection")
        logger.info("5. Verify there are no OpenAI service outages")
        
        return False

if __name__ == "__main__":
    # Run the test
    success = test_llm_connection()
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1) 