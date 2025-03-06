"""
End-to-end test for the chatbot server.

This test verifies that the chatbot server is running and responding to requests.
"""

import pytest
import os
import logging
import requests
import json
import uuid
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TestChatbotServer:
    """
    End-to-end tests for the chatbot server.
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
    
    def test_chatbot_server_response(self, api_url, user_id):
        """Test that the chatbot server responds to a request."""
        # Create a test message
        message = "Hello, can you help me with a website project?"
        
        # Create the payload
        payload = {
            "user_id": user_id,
            "message": message
        }
        
        logger.info(f"Testing chatbot server at {api_url}")
        logger.info(f"Sending message: {message}")
        
        try:
            # Send the request with a timeout of 30 seconds
            response = requests.post(api_url, json=payload, timeout=30)
            
            # Check if the request was successful
            assert response.status_code == 200, f"Request failed with status code: {response.status_code}"
            
            # Parse the response
            response_data = response.json()
            
            # Log the response
            logger.info(f"Response status code: {response.status_code}")
            logger.info(f"Response: {json.dumps(response_data, indent=2)}")
            
            # Check if the response contains the expected fields
            assert "response" in response_data, "Response does not contain the expected 'response' field"
            assert "session_id" in response_data, "Response does not contain the expected 'session_id' field"
            assert "timestamp" in response_data, "Response does not contain the expected 'timestamp' field"
            
            # Check that the response is not empty
            assert response_data["response"], "Response is empty"
            
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out. The server might be taking too long to respond.")
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request failed: {str(e)}")
    
    def test_chatbot_server_session_persistence(self, api_url, user_id):
        """Test that the chatbot server maintains session context."""
        # First message
        first_message = "Hello, I need a website for my business."
        
        # Create the payload for the first message
        first_payload = {
            "user_id": user_id,
            "message": first_message
        }
        
        logger.info(f"Testing session persistence at {api_url}")
        logger.info(f"Sending first message: {first_message}")
        
        try:
            # Send the first request
            first_response = requests.post(api_url, json=first_payload, timeout=30)
            
            # Check if the request was successful
            assert first_response.status_code == 200, f"First request failed with status code: {first_response.status_code}"
            
            # Parse the response
            first_response_data = first_response.json()
            
            # Get the session ID
            session_id = first_response_data["session_id"]
            
            # Second message
            second_message = "It's for a software development company."
            
            # Create the payload for the second message
            second_payload = {
                "user_id": user_id,
                "message": second_message,
                "session_id": session_id
            }
            
            logger.info(f"Sending second message: {second_message}")
            
            # Send the second request
            second_response = requests.post(api_url, json=second_payload, timeout=30)
            
            # Check if the request was successful
            assert second_response.status_code == 200, f"Second request failed with status code: {second_response.status_code}"
            
            # Parse the response
            second_response_data = second_response.json()
            
            # Check that the session ID is the same
            assert second_response_data["session_id"] == session_id, "Session ID changed between requests"
            
            # Check that the response is not empty
            assert second_response_data["response"], "Second response is empty"
            
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out. The server might be taking too long to respond.")
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request failed: {str(e)}") 