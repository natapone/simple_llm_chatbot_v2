"""
Unit tests for the guidance tools module.

These tests verify that the guidance tools correctly retrieve and format guidance information.
"""

import pytest
import os
import json
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the parent directory to the path so we can import from app
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.guidance_tools import (
    get_budget_guidance,
    get_timeline_guidance,
    initialize_guidance_data
)

@pytest.fixture
def sample_budget_guidance():
    """
    Returns sample budget guidance data.
    """
    return [
        {
            "project_type": "e-commerce",
            "min_budget": 3000,
            "max_budget": 8000,
            "description": "Online store with product listings and payment processing"
        },
        {
            "project_type": "corporate",
            "min_budget": 1500,
            "max_budget": 3000,
            "description": "Professional business website with company information"
        },
        {
            "project_type": "blog",
            "min_budget": 1000,
            "max_budget": 2000,
            "description": "Content-focused website with blog posts and articles"
        }
    ]

@pytest.fixture
def sample_timeline_guidance():
    """
    Returns sample timeline guidance data.
    """
    return [
        {
            "project_type": "e-commerce",
            "min_timeline": "1 month",
            "max_timeline": "3 months",
            "description": "Online store with product listings and payment processing"
        },
        {
            "project_type": "corporate",
            "min_timeline": "2 weeks",
            "max_timeline": "4 weeks",
            "description": "Professional business website with company information"
        },
        {
            "project_type": "blog",
            "min_timeline": "1 week",
            "max_timeline": "3 weeks",
            "description": "Content-focused website with blog posts and articles"
        }
    ]

@patch('app.guidance_tools.DatabaseHandler')
def test_get_budget_guidance_all(mock_db_handler, sample_budget_guidance):
    """
    Test that get_budget_guidance returns all budget guidance when no project type is specified.
    """
    # Configure mock
    mock_instance = MagicMock()
    mock_db_handler.return_value = mock_instance
    mock_instance.get_table_data.return_value = sample_budget_guidance
    
    # Call function
    guidance = get_budget_guidance()
    
    # Verify result
    assert guidance == sample_budget_guidance
    mock_instance.get_table_data.assert_called_once_with("budget_guidance")

@patch('app.guidance_tools.DatabaseHandler')
def test_get_budget_guidance_specific(mock_db_handler, sample_budget_guidance):
    """
    Test that get_budget_guidance returns specific budget guidance when a project type is specified.
    """
    # Configure mock
    mock_instance = MagicMock()
    mock_db_handler.return_value = mock_instance
    mock_instance.query_table.return_value = [sample_budget_guidance[0]]
    
    # Call function
    guidance = get_budget_guidance("e-commerce")
    
    # Verify result
    assert guidance == [sample_budget_guidance[0]]
    mock_instance.query_table.assert_called_once_with("budget_guidance", "project_type", "e-commerce")

@patch('app.guidance_tools.DatabaseHandler')
def test_get_budget_guidance_not_found(mock_db_handler):
    """
    Test that get_budget_guidance returns an empty list when no guidance is found.
    """
    # Configure mock
    mock_instance = MagicMock()
    mock_db_handler.return_value = mock_instance
    mock_instance.query_table.return_value = []
    
    # Call function
    guidance = get_budget_guidance("nonexistent")
    
    # Verify result
    assert guidance == []
    mock_instance.query_table.assert_called_once_with("budget_guidance", "project_type", "nonexistent")

@patch('app.guidance_tools.DatabaseHandler')
def test_get_timeline_guidance_all(mock_db_handler, sample_timeline_guidance):
    """
    Test that get_timeline_guidance returns all timeline guidance when no project type is specified.
    """
    # Configure mock
    mock_instance = MagicMock()
    mock_db_handler.return_value = mock_instance
    mock_instance.get_table_data.return_value = sample_timeline_guidance
    
    # Call function
    guidance = get_timeline_guidance()
    
    # Verify result
    assert guidance == sample_timeline_guidance
    mock_instance.get_table_data.assert_called_once_with("timeline_guidance")

@patch('app.guidance_tools.DatabaseHandler')
def test_get_timeline_guidance_specific(mock_db_handler, sample_timeline_guidance):
    """
    Test that get_timeline_guidance returns specific timeline guidance when a project type is specified.
    """
    # Configure mock
    mock_instance = MagicMock()
    mock_db_handler.return_value = mock_instance
    mock_instance.query_table.return_value = [sample_timeline_guidance[0]]
    
    # Call function
    guidance = get_timeline_guidance("e-commerce")
    
    # Verify result
    assert guidance == [sample_timeline_guidance[0]]
    mock_instance.query_table.assert_called_once_with("timeline_guidance", "project_type", "e-commerce")

@patch('app.guidance_tools.DatabaseHandler')
def test_get_timeline_guidance_not_found(mock_db_handler):
    """
    Test that get_timeline_guidance returns an empty list when no guidance is found.
    """
    # Configure mock
    mock_instance = MagicMock()
    mock_db_handler.return_value = mock_instance
    mock_instance.query_table.return_value = []
    
    # Call function
    guidance = get_timeline_guidance("nonexistent")
    
    # Verify result
    assert guidance == []
    mock_instance.query_table.assert_called_once_with("timeline_guidance", "project_type", "nonexistent")

@patch('app.guidance_tools.DatabaseHandler')
def test_initialize_guidance_data(mock_db_handler, sample_budget_guidance, sample_timeline_guidance):
    """
    Test that initialize_guidance_data initializes guidance data in the database.
    """
    # Configure mock
    mock_instance = MagicMock()
    mock_db_handler.return_value = mock_instance
    
    # Call function
    initialize_guidance_data("test_db.json", "test_seed_data.json")
    
    # Verify result
    mock_db_handler.assert_called_once_with("test_db.json")
    assert mock_instance.add_document.call_count >= 6  # 3 budget + 3 timeline guidance entries 