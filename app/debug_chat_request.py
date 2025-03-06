#!/usr/bin/env python3
"""
Debug Chat Request Script

This script sends a request to the chat endpoint and prints detailed information
about the request and response, including any errors.
"""

import os
import sys
import json
import uuid
import logging
import requests
import traceback
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

def debug_chat_request():
    """Send a request to the chat endpoint and print detailed information."""
    # Load environment variables
    load_dotenv(override=True)
    
    # Get API host and port from environment or use defaults
    api_host = os.getenv("API_HOST", "localhost")
    api_port = os.getenv("PORT", "8000")
    
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
    logging.info(f"User ID: {user_id}")
    logging.info(f"Sending message: {message}")
    logging.info(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        # Send the request with a timeout of 30 seconds
        logging.info("Sending request...")
        response = requests.post(api_url, json=payload, timeout=30)
        
        # Log the response status code
        logging.info(f"Response status code: {response.status_code}")
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response
            try:
                response_data = response.json()
                logging.info(f"Response: {json.dumps(response_data, indent=2)}")
                
                # Check if the response contains the expected fields
                if "response" in response_data:
                    logging.info("Test successful! Chatbot server is working correctly.")
                else:
                    logging.error("Response does not contain the expected 'response' field.")
            except json.JSONDecodeError:
                logging.error("Failed to parse response as JSON.")
                logging.error(f"Response text: {response.text}")
        else:
            # Log the error
            logging.error(f"Request failed with status code: {response.status_code}")
            logging.error(f"Response: {response.text}")
            
    except requests.exceptions.Timeout:
        logging.error("Request timed out. The server might be taking too long to respond.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {str(e)}")
        logging.error(traceback.format_exc())
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    # Run the test
    debug_chat_request() 