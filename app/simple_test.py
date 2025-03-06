#!/usr/bin/env python3
"""
Simple Test Script

This script makes a single request to the chatbot API and prints the response.
"""

import os
import requests
import json
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Configuration
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = int(os.getenv("PORT", 8000))
API_URL = f"http://{API_HOST}:{API_PORT}/chat"

def test_chat_api():
    """Test the chat API with a simple message."""
    # Generate a user ID
    user_id = str(uuid.uuid4())
    
    # Create the payload
    payload = {
        "user_id": user_id,
        "message": "Hello, I'm interested in building a website.",
        "session_id": None
    }
    
    print(f"Sending request to {API_URL}...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        # Send the request
        response = requests.post(API_URL, json=payload, timeout=30)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            print("\nResponse:")
            print(f"Status Code: {response.status_code}")
            print(f"Response Data: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"\nError: Status Code {response.status_code}")
            print(f"Response: {response.text}")
            return False
    
    except requests.exceptions.Timeout:
        print("\nError: Request timed out after 30 seconds")
        return False
    
    except requests.exceptions.RequestException as e:
        print(f"\nError: {str(e)}")
        return False

if __name__ == "__main__":
    test_chat_api() 