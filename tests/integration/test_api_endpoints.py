"""
Integration tests for the FastAPI endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import the app
from app.main import app


class TestAPIEndpoints:
    """
    Test cases for the FastAPI endpoints.
    """

    @pytest.fixture
    def client(self):
        """
        Returns a TestClient instance.
        """
        return TestClient(app)

    def test_root_endpoint(self, client):
        """
        Test that the root endpoint returns a 200 status code and HTML content.
        """
        response = client.get("/")
        
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "<html" in response.text.lower()

    @patch('app.main.ChatHandler')
    def test_chat_endpoint_valid_request(self, mock_chat_handler, client):
        """
        Test that the chat endpoint processes a valid request correctly.
        """
        # Set up mock
        mock_handler = MagicMock()
        mock_chat_handler.return_value = mock_handler
        
        mock_handler.process_message.return_value = {
            "response": "This is a test response.",
            "session_id": "test-session-123"
        }
        
        # Test data
        request_data = {
            "message": "Hello, I need help with a project",
            "session_id": "test-session-123"
        }
        
        # Call the endpoint
        response = client.post("/chat", json=request_data)
        
        # Verify the response
        assert response.status_code == 200
        assert response.json() == {
            "response": "This is a test response.",
            "session_id": "test-session-123"
        }
        
        # Verify that the chat handler was called correctly
        mock_handler.process_message.assert_called_once_with(
            "Hello, I need help with a project",
            "test-session-123"
        )

    @patch('app.main.ChatHandler')
    def test_chat_endpoint_no_session_id(self, mock_chat_handler, client):
        """
        Test that the chat endpoint handles a request without a session ID correctly.
        """
        # Set up mock
        mock_handler = MagicMock()
        mock_chat_handler.return_value = mock_handler
        
        mock_handler.generate_session_id.return_value = "new-session-123"
        mock_handler.process_message.return_value = {
            "response": "This is a test response.",
            "session_id": "new-session-123"
        }
        
        # Test data
        request_data = {
            "message": "Hello, I need help with a project"
        }
        
        # Call the endpoint
        response = client.post("/chat", json=request_data)
        
        # Verify the response
        assert response.status_code == 200
        assert response.json() == {
            "response": "This is a test response.",
            "session_id": "new-session-123"
        }
        
        # Verify that the chat handler was called correctly
        mock_handler.generate_session_id.assert_called_once()
        mock_handler.process_message.assert_called_once_with(
            "Hello, I need help with a project",
            "new-session-123"
        )

    def test_chat_endpoint_missing_message(self, client):
        """
        Test that the chat endpoint returns a 422 status code for a request without a message.
        """
        # Test data
        request_data = {
            "session_id": "test-session-123"
        }
        
        # Call the endpoint
        response = client.post("/chat", json=request_data)
        
        # Verify the response
        assert response.status_code == 422
        assert "detail" in response.json()
        assert "message" in response.json()["detail"][0]["loc"]

    @patch('app.main.ChatHandler')
    def test_chat_endpoint_error_handling(self, mock_chat_handler, client):
        """
        Test that the chat endpoint handles errors correctly.
        """
        # Set up mock
        mock_handler = MagicMock()
        mock_chat_handler.return_value = mock_handler
        
        mock_handler.process_message.side_effect = Exception("Test error")
        
        # Test data
        request_data = {
            "message": "Hello, I need help with a project",
            "session_id": "test-session-123"
        }
        
        # Call the endpoint
        response = client.post("/chat", json=request_data)
        
        # Verify the response
        assert response.status_code == 500
        assert "detail" in response.json()
        assert "error processing chat message" in response.json()["detail"].lower()
        
        # Verify that the chat handler was called
        mock_handler.process_message.assert_called_once() 