"""
Integration tests for the LLM integration.

These tests verify that the application correctly interacts with the LLM via LiteLLM.
Note: These tests require a valid LLM API key and will make actual API calls.
"""

import pytest
import os
import json
from typing import Dict, Any, List
import litellm
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import from app
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.chat_handler import process_chat_message
from app.database_handler import DatabaseHandler


class TestLLMIntegration:
    """
    Integration tests for the LLM integration.
    """
    
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
    def llm_api_key(self):
        """
        Returns the LLM API key from environment variables.
        """
        api_key = os.getenv("LLM_API_KEY")
        if not api_key:
            pytest.skip("LLM_API_KEY environment variable not set")
        
        return api_key
    
    @pytest.fixture
    def llm_provider(self):
        """
        Returns the LLM provider from environment variables.
        """
        provider = os.getenv("LLM_PROVIDER", "openai")
        return provider
    
    @pytest.fixture
    def llm_model(self):
        """
        Returns the LLM model from environment variables.
        """
        model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        return model
    
    @pytest.fixture
    def test_user_id(self):
        """
        Returns a test user ID.
        """
        return "test_user_integration"
    
    def test_litellm_direct_completion(self, llm_api_key, llm_provider, llm_model):
        """
        Test direct completion with LiteLLM.
        """
        # Set API key
        os.environ["OPENAI_API_KEY"] = llm_api_key
        
        # Create a simple prompt
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"}
        ]
        
        # Call LiteLLM directly
        response = litellm.completion(
            model=f"{llm_provider}/{llm_model}",
            messages=messages,
            max_tokens=100
        )
        
        # Verify response
        assert response is not None
        assert "choices" in response
        assert len(response["choices"]) > 0
        assert "message" in response["choices"][0]
        assert "content" in response["choices"][0]["message"]
        assert len(response["choices"][0]["message"]["content"]) > 0
    
    def test_process_chat_message(self, test_db, test_user_id, llm_api_key, llm_provider, llm_model):
        """
        Test processing a chat message through the chat handler.
        """
        # Set API key
        os.environ["OPENAI_API_KEY"] = llm_api_key
        os.environ["LLM_PROVIDER"] = llm_provider
        os.environ["LLM_MODEL"] = llm_model
        
        # Process a simple message
        message = "Hello, I'm interested in building a website for my business."
        session_id = None  # Let the handler generate a session ID
        
        # Call the process_chat_message function
        response, new_session_id = process_chat_message(
            test_user_id,
            message,
            session_id,
            test_db
        )
        
        # Verify response
        assert response is not None
        assert len(response) > 0
        assert new_session_id is not None
        assert len(new_session_id) > 0
        
        # Process a follow-up message using the same session ID
        follow_up_message = "It's a small clothing store, and I want to sell products online."
        
        # Call the process_chat_message function again
        follow_up_response, _ = process_chat_message(
            test_user_id,
            follow_up_message,
            new_session_id,
            test_db
        )
        
        # Verify follow-up response
        assert follow_up_response is not None
        assert len(follow_up_response) > 0
        
        # The follow-up response should reference the previous message context
        # This is hard to test deterministically, but we can check for common patterns
        # in responses to e-commerce inquiries
        e_commerce_terms = ["e-commerce", "online store", "products", "shop", "website"]
        has_context = any(term.lower() in follow_up_response.lower() for term in e_commerce_terms)
        
        assert has_context, "Follow-up response doesn't seem to maintain conversation context"
    
    def test_system_prompt_guidance(self, test_db, test_user_id, llm_api_key, llm_provider, llm_model):
        """
        Test that the system prompt correctly guides the LLM's responses.
        """
        # Set API key
        os.environ["OPENAI_API_KEY"] = llm_api_key
        os.environ["LLM_PROVIDER"] = llm_provider
        os.environ["LLM_MODEL"] = llm_model
        
        # Process a message asking about budget
        message = "How much would it cost to build an e-commerce website?"
        session_id = None  # Let the handler generate a session ID
        
        # Call the process_chat_message function
        response, new_session_id = process_chat_message(
            test_user_id,
            message,
            session_id,
            test_db
        )
        
        # Verify response contains budget information
        budget_terms = ["budget", "cost", "price", "$", "dollars", "investment"]
        has_budget_info = any(term.lower() in response.lower() for term in budget_terms)
        
        assert has_budget_info, "Response doesn't contain budget information"
        
        # Process a message asking about timeline
        message = "How long would it take to build an e-commerce website?"
        
        # Call the process_chat_message function
        response, _ = process_chat_message(
            test_user_id,
            message,
            new_session_id,
            test_db
        )
        
        # Verify response contains timeline information
        timeline_terms = ["timeline", "time", "weeks", "months", "development", "schedule"]
        has_timeline_info = any(term.lower() in response.lower() for term in timeline_terms)
        
        assert has_timeline_info, "Response doesn't contain timeline information"
    
    def test_conversation_history_persistence(self, test_db, test_user_id, llm_api_key, llm_provider, llm_model):
        """
        Test that conversation history is correctly persisted in the database.
        """
        # Set API key
        os.environ["OPENAI_API_KEY"] = llm_api_key
        os.environ["LLM_PROVIDER"] = llm_provider
        os.environ["LLM_MODEL"] = llm_model
        
        # Process a message
        message = "Hi, I need a mobile app for my restaurant."
        session_id = None  # Let the handler generate a session ID
        
        # Call the process_chat_message function
        response, new_session_id = process_chat_message(
            test_user_id,
            message,
            session_id,
            test_db
        )
        
        # Verify conversation was stored in the database
        conversations = test_db.query_table("conversations", "session_id", new_session_id)
        
        # Verify conversation data
        assert len(conversations) > 0
        conversation = conversations[0]
        assert "user_id" in conversation
        assert conversation["user_id"] == test_user_id
        assert "session_id" in conversation
        assert conversation["session_id"] == new_session_id
        assert "messages" in conversation
        assert len(conversation["messages"]) >= 2  # System prompt + user message
        
        # Verify user message
        user_messages = [msg for msg in conversation["messages"] if msg.get("role") == "user"]
        assert len(user_messages) > 0
        assert user_messages[0]["content"] == message
        
        # Verify assistant message
        assistant_messages = [msg for msg in conversation["messages"] if msg.get("role") == "assistant"]
        assert len(assistant_messages) > 0
        assert assistant_messages[0]["content"] == response 