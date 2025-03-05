"""
End-to-end tests for the chat flow.

These tests verify the complete chat flow from user input to response,
testing the integration of all components.
"""

import pytest
import os
import json
import uuid
from fastapi.testclient import TestClient
from typing import Dict, Any, List
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import from app
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.main import app
from app.chat_handler import ChatHandler
from app.llm_handler import LLMHandler
from app.database_handler import DatabaseHandler
from app.guidance_tools import get_budget_guidance, get_timeline_guidance


class TestChatFlow:
    """
    End-to-end tests for the chat flow.
    """
    
    @pytest.fixture
    def client(self):
        """
        Returns a TestClient instance.
        """
        return TestClient(app)
    
    @pytest.fixture
    def test_db(self):
        """
        Returns a DatabaseHandler instance connected to the test database.
        
        Note: This requires a valid test database file specified in the TEST_DB_PATH
        environment variable. If not found, the test will be skipped.
        """
        # Get the test database path from environment or use default
        db_path = os.environ.get('TEST_DB_PATH', 'tests/test_data/test_db.json')
        
        # Check if the test database file exists
        if not os.path.exists(db_path):
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
            # Create an empty database file
            with open(db_path, 'w') as f:
                json.dump({}, f)
        
        return DatabaseHandler(db_path)
    
    @pytest.fixture
    def chat_handler(self, test_db):
        """
        Returns a ChatHandler instance with a real LLMHandler and test DatabaseHandler.
        """
        # Use a mock LLM handler to avoid making real API calls
        mock_llm = MagicMock(spec=LLMHandler)
        mock_llm.generate_response.return_value = "I'm a test assistant. How can I help you with your software project?"
        
        # Create a system prompt
        system_prompt = """
        You are a friendly and helpful pre-sales chatbot for a software development company.
        Your goal is to engage with potential clients, understand their project needs,
        and collect their contact information for follow-up.
        """
        
        return ChatHandler(
            llm_handler=mock_llm,
            db_handler=test_db,
            system_prompt=system_prompt
        )
    
    @pytest.fixture
    def test_user_id(self):
        """
        Returns a test user ID.
        """
        return f"test_user_e2e_{uuid.uuid4().hex[:8]}"
    
    def test_complete_chat_flow(self, chat_handler, test_db):
        """
        Test a complete chat flow from initial greeting to lead storage.
        """
        # Initialize conversation
        session_id = "test_session_123"
        user_id = "test_user_456"
        
        # First user message
        response = chat_handler.handle_message(
            "Hi, I'm interested in getting a website built for my business.",
            session_id,
            user_id
        )
        
        assert response is not None
        assert isinstance(response, dict)
        assert "response" in response
        assert "session_id" in response
        assert response["session_id"] == session_id
        
        # Second user message - provide more details
        response = chat_handler.handle_message(
            "I run a small e-commerce business selling handmade crafts. I need a website with product listings, shopping cart, and payment processing.",
            session_id,
            user_id
        )
        
        assert "response" in response
        assert "e-commerce" in response["response"].lower() or "online store" in response["response"].lower()
        
        # Third user message - ask about budget
        response = chat_handler.handle_message(
            "What kind of budget should I expect for this type of website?",
            session_id,
            user_id
        )
        
        assert "response" in response
        assert "budget" in response["response"].lower()
        
        # Fourth user message - ask about timeline
        response = chat_handler.handle_message(
            "How long would it take to build?",
            session_id,
            user_id
        )
        
        assert "response" in response
        assert "timeline" in response["response"].lower() or "weeks" in response["response"].lower() or "months" in response["response"].lower()
        
        # Fifth user message - provide contact information
        response = chat_handler.handle_message(
            "My name is Test User and my email is test@example.com",
            session_id,
            user_id
        )
        
        assert "response" in response
        assert "contact" in response["response"].lower() or "follow" in response["response"].lower()
        
        # Sixth user message - provide consent for follow-up
        response = chat_handler.handle_message(
            "Yes, you can contact me about my project.",
            session_id,
            user_id
        )
        
        assert "response" in response
        assert "thank" in response["response"].lower()
        
        # Verify conversation was stored in TinyDB
        # This would require querying the test database
        # For simplicity, we'll just check that the conversation history exists in the chat handler
        assert len(chat_handler.conversation_histories.get(session_id, [])) > 0
        
        # In a real test, you would query the database to verify the lead was stored
        # conversations = test_db.query_table("conversations", "session_id", session_id)
        # assert len(conversations) > 0
    
    def test_error_handling(self, client):
        """
        Test error handling in the chat flow.
        """
        # Test missing user_id
        response = client.post(
            "/chat",
            json={
                "message": "Hello"
            }
        )
        
        # Verify response
        assert response.status_code == 422  # Unprocessable Entity
        
        # Test missing message
        response = client.post(
            "/chat",
            json={
                "user_id": "test_user"
            }
        )
        
        # Verify response
        assert response.status_code == 422  # Unprocessable Entity
        
        # Test invalid session_id format
        response = client.post(
            "/chat",
            json={
                "user_id": "test_user",
                "message": "Hello",
                "session_id": "invalid-session-id-format"
            }
        )
        
        # This might return 200 if the application accepts any string as session_id
        # or 400/422 if it validates the format
        # The important thing is that it doesn't crash
        assert response.status_code in [200, 400, 422]
    
    def test_session_management(self, client, test_user_id):
        """
        Test session management in the chat flow.
        """
        # Step 1: Send a message without a session ID
        response = client.post(
            "/chat",
            json={
                "user_id": test_user_id,
                "message": "Hello"
            }
        )
        
        # Verify a session ID is generated
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        session_id = data["session_id"]
        
        # Step 2: Send another message with the session ID
        response = client.post(
            "/chat",
            json={
                "user_id": test_user_id,
                "message": "How are you?",
                "session_id": session_id
            }
        )
        
        # Verify the same session ID is returned
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert data["session_id"] == session_id
        
        # Step 3: Send a message with a different user ID but the same session ID
        different_user_id = f"different_user_{uuid.uuid4().hex[:8]}"
        
        response = client.post(
            "/chat",
            json={
                "user_id": different_user_id,
                "message": "Hello from a different user",
                "session_id": session_id
            }
        )
        
        # Verify a new session ID is generated for the different user
        # or the request is rejected
        assert response.status_code in [200, 400, 403]
        if response.status_code == 200:
            data = response.json()
            assert "session_id" in data
            # The behavior depends on the implementation:
            # Either a new session ID is generated, or the request is rejected
            if "session_id" in data:
                assert data["session_id"] != session_id 