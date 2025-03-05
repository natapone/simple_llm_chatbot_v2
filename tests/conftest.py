"""
Common test fixtures for the Simple LLM Chatbot v2 tests.

This file contains fixtures that can be reused across different test modules.
"""

import pytest
import os
import json
import uuid
from datetime import datetime
from unittest.mock import MagicMock, patch
from typing import Dict, Any, List, Optional

from fastapi.testclient import TestClient
from app.main import app
from app.chat_handler import ChatHandler
from app.llm_handler import LLMHandler
from app.database_handler import DatabaseHandler
from app.guidance_tools import get_budget_guidance, get_timeline_guidance

# Add the parent directory to the path so we can import from app
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def test_client():
    """
    Returns a TestClient instance for the FastAPI app.
    """
    return TestClient(app)

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
def test_db_path():
    """
    Returns the path to the test database file.
    """
    return os.path.join(os.path.dirname(__file__), "test_data", "test_db.json")

@pytest.fixture
def mock_chat_handler(mock_llm_handler, mock_db_handler):
    """
    Returns a mocked ChatHandler instance.
    """
    handler = ChatHandler(
        llm_handler=mock_llm_handler,
        db_handler=mock_db_handler,
        system_prompt="You are a test assistant."
    )
    return handler

@pytest.fixture
def test_conversation_history():
    """
    Returns a test conversation history.
    """
    return [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, I need help with a project."},
        {"role": "assistant", "content": "I'd be happy to help. What kind of project are you working on?"},
        {"role": "user", "content": "I need a website for my business."}
    ]

@pytest.fixture
def test_lead_data():
    """
    Returns test lead data.
    """
    return {
        "client_name": "Test User",
        "client_business": "Test Business",
        "contact_information": "test@example.com",
        "project_description": "A website for my business",
        "features": ["contact form", "about page"],
        "timeline": "2 months",
        "budget_range": "$5,000-$10,000",
        "confirmed_follow_up": True
    }

@pytest.fixture
def mock_litellm():
    """
    Returns a mocked litellm module.
    """
    with patch("litellm.completion") as mock_completion:
        mock_completion.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "This is a mock response from the LLM.",
                        "role": "assistant"
                    },
                    "index": 0,
                    "finish_reason": "stop"
                }
            ],
            "created": int(datetime.now().timestamp()),
            "model": "mock-model",
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 20,
                "total_tokens": 30
            }
        }
        yield mock_completion

@pytest.fixture
def sample_chat_message():
    """
    Returns a sample chat message.
    """
    return {
        "user_id": "test_user",
        "message": "Hello, I need help with a project",
        "session_id": "test-session-123"
    }

@pytest.fixture
def sample_conversation_history():
    """
    Returns a sample conversation history.
    """
    return {
        "user_id": "test_user",
        "session_id": "test-session-123",
        "messages": [
            {
                "role": "system",
                "content": "You are a friendly and helpful pre-sales chatbot for a software development company."
            },
            {
                "role": "user",
                "content": "Hello, I need help with a project"
            },
            {
                "role": "assistant",
                "content": "Hi there! I'd be happy to help with your project. Could you tell me more about what you're looking to build?"
            },
            {
                "role": "user",
                "content": "I need a website for my business"
            },
            {
                "role": "assistant",
                "content": "Great! I'd be happy to discuss a website for your business. What kind of business do you have, and what are the main features you'd like on your website?"
            }
        ],
        "created_at": "2023-03-06T14:30:00Z",
        "updated_at": "2023-03-06T14:35:00Z"
    }

@pytest.fixture
def sample_budget_guidance():
    """
    Returns sample budget guidance data.
    """
    return [
        {
            "project_type": "Basic website",
            "min_budget": 1500,
            "max_budget": 3000,
            "description": "Simple informational website with a few pages"
        },
        {
            "project_type": "E-commerce site",
            "min_budget": 3000,
            "max_budget": 8000,
            "description": "Online store with product listings and payment processing"
        },
        {
            "project_type": "Mobile app",
            "min_budget": 5000,
            "max_budget": 15000,
            "description": "Native or cross-platform mobile application"
        },
        {
            "project_type": "Custom software",
            "min_budget": 10000,
            "max_budget": 50000,
            "description": "Bespoke software solution for specific business needs"
        }
    ]

@pytest.fixture
def sample_timeline_guidance():
    """
    Returns sample timeline guidance data.
    """
    return [
        {
            "project_type": "Basic website",
            "min_timeline": "2 weeks",
            "max_timeline": "4 weeks",
            "description": "Simple informational website with a few pages"
        },
        {
            "project_type": "E-commerce site",
            "min_timeline": "1 month",
            "max_timeline": "3 months",
            "description": "Online store with product listings and payment processing"
        },
        {
            "project_type": "Mobile app",
            "min_timeline": "2 months",
            "max_timeline": "4 months",
            "description": "Native or cross-platform mobile application"
        },
        {
            "project_type": "Custom software",
            "min_timeline": "3 months",
            "max_timeline": "6 months",
            "description": "Bespoke software solution for specific business needs"
        }
    ] 