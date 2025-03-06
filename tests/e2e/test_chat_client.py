"""
End-to-end test for the chat client.

This test verifies that the chat client can communicate with the chatbot server.
"""

import pytest
import os
import logging
import requests
import uuid
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TestChatClient:
    """
    End-to-end tests for the chat client.
    """
    
    @pytest.fixture
    def api_url(self):
        """Fixture for API URL."""
        # Load environment variables
        load_dotenv()
        
        # Get API host and port from environment or use defaults
        api_host = os.getenv("API_HOST", "localhost")
        api_port = os.getenv("API_PORT", "8000")
        
        # Construct the API URL
        return f"http://{api_host}:{api_port}/chat"
    
    @pytest.fixture
    def user_id(self):
        """Fixture for user ID."""
        return str(uuid.uuid4())
    
    def chat_with_bot(self, api_url, user_id, message, session_id=None):
        """
        Send a message to the chatbot API and return the response.
        
        Args:
            api_url: The URL of the chatbot API
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
            response = requests.post(api_url, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            data = response.json()
            return data["response"], data["session_id"]
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error communicating with the API: {str(e)}")
            return None, session_id
    
    def test_chat_client_single_message(self, api_url, user_id):
        """Test that the chat client can send a single message and receive a response."""
        # Test message
        message = "Hello, can you help me with a website project?"
        
        # Send the message to the chatbot
        response, session_id = self.chat_with_bot(api_url, user_id, message)
        
        # Verify the response
        assert response is not None, "No response from the chatbot"
        assert isinstance(response, str), "Response is not a string"
        assert len(response) > 0, "Response is empty"
        assert session_id is not None, "No session ID returned"
    
    def test_chat_client_conversation(self, api_url, user_id):
        """Test that the chat client can have a conversation with the chatbot."""
        # First message
        first_message = "Hello, I need a website for my business."
        
        # Send the first message to the chatbot
        first_response, session_id = self.chat_with_bot(api_url, user_id, first_message)
        
        # Verify the first response
        assert first_response is not None, "No response from the chatbot for the first message"
        assert session_id is not None, "No session ID returned for the first message"
        
        # Second message
        second_message = "It's for a software development company."
        
        # Send the second message to the chatbot
        second_response, updated_session_id = self.chat_with_bot(api_url, user_id, second_message, session_id)
        
        # Verify the second response
        assert second_response is not None, "No response from the chatbot for the second message"
        assert updated_session_id == session_id, "Session ID changed between messages"
        
        # Third message
        third_message = "I need it to showcase our services and allow clients to contact us."
        
        # Send the third message to the chatbot
        third_response, final_session_id = self.chat_with_bot(api_url, user_id, third_message, updated_session_id)
        
        # Verify the third response
        assert third_response is not None, "No response from the chatbot for the third message"
        assert final_session_id == updated_session_id, "Session ID changed between messages" 