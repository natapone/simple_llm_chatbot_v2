"""
Unit tests for the chat_handler module.

These tests verify that the chat handler correctly processes messages and manages conversation state.
"""

import pytest
import os
import json
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the parent directory to the path so we can import from app
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.chat_handler import ChatHandler
from app.llm_handler import LLMHandler
from app.database_handler import DatabaseHandler

@pytest.fixture
def mock_llm_handler():
    """
    Returns a mocked LLMHandler instance.
    """
    mock_handler = MagicMock(spec=LLMHandler)
    mock_handler.generate_response.return_value = "This is a test response"
    return mock_handler

@pytest.fixture
def mock_db_handler():
    """
    Returns a mocked DatabaseHandler instance.
    """
    mock_handler = MagicMock(spec=DatabaseHandler)
    mock_handler.add_document.return_value = "test_doc_id"
    mock_handler.get_document.return_value = {"content": "test content"}
    mock_handler.query_table.return_value = [{"id": "1", "content": "test content"}]
    return mock_handler

@pytest.fixture
def chat_handler(mock_llm_handler, mock_db_handler):
    """
    Returns a ChatHandler instance with mocked dependencies.
    """
    return ChatHandler(
        llm_handler=mock_llm_handler,
        db_handler=mock_db_handler,
        system_prompt="You are a test assistant."
    )

@patch('app.chat_handler.DatabaseHandler')
def test_get_system_prompt(mock_db_handler):
    """
    Test that get_system_prompt retrieves the system prompt from the database.
    """
    # Configure mock
    mock_instance = MagicMock()
    mock_db_handler.return_value = mock_instance
    mock_instance.get_document.return_value = {
        "content": "You are a friendly and helpful pre-sales chatbot."
    }
    
    # Create chat handler with mock database
    handler = ChatHandler(
        llm_handler=MagicMock(),
        db_handler=mock_instance,
        system_prompt=None
    )
    
    # Verify system prompt
    assert handler.system_prompt == "You are a friendly and helpful pre-sales chatbot."
    mock_instance.get_document.assert_called_once_with("system_prompts", "default")

@patch('app.chat_handler.DatabaseHandler')
def test_handle_message_new_session(mock_db_handler):
    """
    Test that handle_message creates a new session when none is provided.
    """
    # Configure mock
    mock_instance = MagicMock()
    mock_db_handler.return_value = mock_instance
    
    # Create chat handler with mock database
    mock_llm = MagicMock()
    mock_llm.generate_response.return_value = "Hello! How can I help you?"
    
    handler = ChatHandler(
        llm_handler=mock_llm,
        db_handler=mock_instance,
        system_prompt="You are a test assistant."
    )
    
    # Call handle_message with no session ID
    response = handler.handle_message(
        "Hi there!",
        None,
        "test_user"
    )
    
    # Verify response
    assert response is not None
    assert "response" in response
    assert response["response"] == "Hello! How can I help you!"
    assert "session_id" in response
    assert response["session_id"] is not None

@patch('app.chat_handler.DatabaseHandler')
def test_handle_message_existing_session(mock_db_handler):
    """
    Test that handle_message uses an existing session when provided.
    """
    # Configure mock
    mock_instance = MagicMock()
    mock_db_handler.return_value = mock_instance
    
    # Create chat handler with mock database
    mock_llm = MagicMock()
    mock_llm.generate_response.return_value = "I understand you need a website."
    
    handler = ChatHandler(
        llm_handler=mock_llm,
        db_handler=mock_instance,
        system_prompt="You are a test assistant."
    )
    
    # Set up existing conversation history
    session_id = "test_session_123"
    handler.conversation_histories[session_id] = [
        {"role": "system", "content": "You are a test assistant."},
        {"role": "user", "content": "Hi there!"},
        {"role": "assistant", "content": "Hello! How can I help you?"}
    ]
    
    # Call handle_message with existing session ID
    response = handler.handle_message(
        "I need a website for my business.",
        session_id,
        "test_user"
    )
    
    # Verify response
    assert response is not None
    assert "response" in response
    assert response["response"] == "I understand you need a website."
    assert "session_id" in response
    assert response["session_id"] == session_id

@patch('app.chat_handler.DatabaseHandler')
def test_save_conversation_history(mock_db_handler):
    """
    Test that save_conversation_history saves the conversation history to the database.
    """
    # Configure mock
    mock_instance = MagicMock()
    mock_db_handler.return_value = mock_instance
    mock_instance.add_document.return_value = "test_conversation_id"
    
    # Create chat handler with mock database
    handler = ChatHandler(
        llm_handler=MagicMock(),
        db_handler=mock_instance,
        system_prompt="You are a test assistant."
    )
    
    # Set up conversation history
    session_id = "test_session_123"
    user_id = "test_user_456"
    conversation_history = [
        {"role": "system", "content": "You are a test assistant."},
        {"role": "user", "content": "Hi there!"},
        {"role": "assistant", "content": "Hello! How can I help you?"}
    ]
    
    # Call save_conversation_history
    handler.save_conversation_history(user_id, session_id, conversation_history)
    
    # Verify database call
    mock_instance.add_document.assert_called_once()
    args, kwargs = mock_instance.add_document.call_args
    assert args[0] == "conversations"
    assert "user_id" in args[1]
    assert args[1]["user_id"] == user_id
    assert "session_id" in args[1]
    assert args[1]["session_id"] == session_id
    assert "messages" in args[1]
    assert args[1]["messages"] == conversation_history

def test_extract_lead_info(chat_handler):
    """
    Test that extract_lead_info correctly extracts lead information from conversation history.
    """
    # Set up conversation history
    conversation_history = [
        {"role": "system", "content": "You are a test assistant."},
        {"role": "user", "content": "Hi, I need a website for my business."},
        {"role": "assistant", "content": "I'd be happy to help. What kind of business do you have?"},
        {"role": "user", "content": "I run a small clothing store called Fashion Trends."},
        {"role": "assistant", "content": "Great! What features would you like on your website?"},
        {"role": "user", "content": "I need product listings, a shopping cart, and payment processing."},
        {"role": "assistant", "content": "What's your budget for this project?"},
        {"role": "user", "content": "Around $5,000 to $10,000."},
        {"role": "assistant", "content": "What's your timeline for this project?"},
        {"role": "user", "content": "I'd like to launch in about 2 months."},
        {"role": "assistant", "content": "Can I get your name and email for follow-up?"},
        {"role": "user", "content": "My name is John Smith and my email is john@example.com."},
        {"role": "assistant", "content": "Can we contact you about your project?"},
        {"role": "user", "content": "Yes, that's fine."}
    ]
    
    # Call extract_lead_info
    lead_info = chat_handler.extract_lead_info(conversation_history)
    
    # Verify lead info
    assert lead_info is not None
    assert "client_name" in lead_info
    assert lead_info["client_name"] == "John Smith"
    assert "contact_information" in lead_info
    assert lead_info["contact_information"] == "john@example.com"
    assert "project_description" in lead_info
    assert "budget_range" in lead_info
    assert "$5,000 to $10,000" in lead_info["budget_range"]
    assert "timeline" in lead_info
    assert "2 months" in lead_info["timeline"]
    assert "confirmed_follow_up" in lead_info
    assert lead_info["confirmed_follow_up"] is True 