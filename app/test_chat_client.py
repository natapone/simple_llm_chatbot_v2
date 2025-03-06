#!/usr/bin/env python3
"""
Test Chat Client

A simple command-line client to test the chatbot API.
This script allows you to interact with the chatbot directly from the terminal.
"""

import os
import sys
import json
import uuid
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Configuration
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = int(os.getenv("PORT", 8000))
API_URL = f"http://{API_HOST}:{API_PORT}/chat"

def generate_user_id():
    """Generate a unique user ID for testing."""
    return str(uuid.uuid4())

def chat_with_bot(user_id, message, session_id=None):
    """
    Send a message to the chatbot API and return the response.
    
    Args:
        user_id: The user ID for the conversation
        message: The message to send to the chatbot
        session_id: Optional session ID for continuing a conversation
        
    Returns:
        The chatbot's response and the session ID
    """
    payload = {
        "user_id": user_id,
        "message": message,
        "session_id": session_id
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        data = response.json()
        return data["response"], data["session_id"]
    
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with the API: {str(e)}")
        return None, session_id

def main():
    """Main function to run the chat client."""
    print("=" * 50)
    print("Pre-Sales Chatbot Test Client")
    print("=" * 50)
    print("Type 'exit' or 'quit' to end the conversation.")
    print()
    
    # Generate a user ID for this session
    user_id = generate_user_id()
    print(f"User ID: {user_id}")
    
    # Start with no session ID
    session_id = None
    
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        # Check if the user wants to exit
        if user_input.lower() in ["exit", "quit"]:
            print("\nThank you for using the Pre-Sales Chatbot!")
            break
        
        # Send the message to the chatbot
        bot_response, session_id = chat_with_bot(user_id, user_input, session_id)
        
        if bot_response:
            print(f"\nBot: {bot_response}")
            print(f"Session ID: {session_id}")
        else:
            print("\nNo response from the chatbot. Please try again.")
    
if __name__ == "__main__":
    main() 