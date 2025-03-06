#!/usr/bin/env python3
"""
Test script for the chatbot server.
This script tests the chatbot server by sending a request and checking the response.
"""

import os
import sys
import logging
import requests
import json
import uuid
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

def test_chatbot_server():
    """Test the chatbot server by sending a request and checking the response."""
    # Load environment variables
    load_dotenv(override=True)
    
    # Get API host and port from environment or use defaults
    api_host = os.getenv("API_HOST", "localhost")
    api_port = os.getenv("API_PORT", "8000")
    
    # Construct the API URL
    api_url = f"http://{api_host}:{api_port}/chat"
    
    # Generate a user ID
    user_id = str(uuid.uuid4())
    
    # Create a test message
    message = "Hello, can you help me with a website project?"
    
    # Create the payload
    payload = {
        "user_id": user_id,
        "message": message
    }
    
    logging.info(f"Testing chatbot server at {api_url}")
    logging.info(f"Sending message: {message}")
    
    try:
        # Send the request with a timeout of 30 seconds
        response = requests.post(api_url, json=payload, timeout=30)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response
            response_data = response.json()
            
            # Log the response
            logging.info(f"Response status code: {response.status_code}")
            logging.info(f"Response: {json.dumps(response_data, indent=2)}")
            
            # Check if the response contains the expected fields
            if "response" in response_data:
                logging.info("Test successful! Chatbot server is working correctly.")
                return True
            else:
                logging.error("Response does not contain the expected 'response' field.")
                return False
        else:
            # Log the error
            logging.error(f"Request failed with status code: {response.status_code}")
            logging.error(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        logging.error("Request timed out. The server might be taking too long to respond.")
        return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {str(e)}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    # Run the test
    success = test_chatbot_server()
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1) 