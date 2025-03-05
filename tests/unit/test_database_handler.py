"""
Unit tests for the DatabaseHandler class.

This module contains tests for the TinyDB database handler implementation.
"""

import os
import pytest
import tempfile
import datetime
from unittest.mock import patch, MagicMock
from typing import Dict, List, Any, Optional

# Import the DatabaseHandler class
from app.database_handler import DatabaseHandler

class TestDatabaseHandler:
    """Test cases for the DatabaseHandler class."""
    
    @pytest.fixture
    def temp_db_path(self):
        """Create a temporary database file for testing."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp_file:
            temp_path = temp_file.name
        yield temp_path
        # Clean up the temporary file after the test
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    @pytest.fixture
    def db_handler(self, temp_db_path):
        """Create a DatabaseHandler instance for testing."""
        handler = DatabaseHandler(temp_db_path)
        return handler
    
    def test_init_creates_directory(self, temp_db_path):
        """Test that the constructor creates the directory if it doesn't exist."""
        # Create a path in a non-existent directory
        dir_path = os.path.join(os.path.dirname(temp_db_path), 'test_dir')
        db_path = os.path.join(dir_path, 'test_db.json')
        
        # Initialize the handler, which should create the directory
        handler = DatabaseHandler(db_path)
        
        # Check that the directory was created
        assert os.path.exists(dir_path)
        
        # Clean up
        if os.path.exists(db_path):
            os.remove(db_path)
        os.rmdir(dir_path)
    
    def test_init_initializes_default_data(self, db_handler):
        """Test that the constructor initializes default data in empty tables."""
        # Check that the budget guidance table has data
        budget_data = db_handler.get_table_data('budget_guidance')
        assert len(budget_data) > 0
        
        # Check that the timeline guidance table has data
        timeline_data = db_handler.get_table_data('timeline_guidance')
        assert len(timeline_data) > 0
    
    def test_get_document_existing(self, db_handler):
        """Test retrieving an existing document."""
        # Add a test document
        test_data = {"name": "Test Document", "value": 123}
        doc_id = db_handler.add_document("test", test_data)
        
        # Retrieve the document
        doc = db_handler.get_document("test", str(doc_id))
        
        # Check that the document was retrieved correctly
        assert doc is not None
        assert doc["name"] == "Test Document"
        assert doc["value"] == 123
    
    def test_get_document_non_existing(self, db_handler):
        """Test retrieving a non-existing document."""
        # Try to retrieve a document that doesn't exist
        doc = db_handler.get_document("test", "999")
        
        # Check that None is returned
        assert doc is None
    
    def test_get_table_data(self, db_handler):
        """Test retrieving all documents from a table."""
        # Add some test documents
        db_handler.add_document("test", {"name": "Doc 1", "value": 1})
        db_handler.add_document("test", {"name": "Doc 2", "value": 2})
        db_handler.add_document("test", {"name": "Doc 3", "value": 3})
        
        # Retrieve all documents
        docs = db_handler.get_table_data("test")
        
        # Check that all documents were retrieved
        assert len(docs) == 3
        assert any(doc["name"] == "Doc 1" for doc in docs)
        assert any(doc["name"] == "Doc 2" for doc in docs)
        assert any(doc["name"] == "Doc 3" for doc in docs)
    
    def test_query_table(self, db_handler):
        """Test querying documents in a table."""
        # Add some test documents
        db_handler.add_document("test", {"name": "Doc 1", "category": "A"})
        db_handler.add_document("test", {"name": "Doc 2", "category": "B"})
        db_handler.add_document("test", {"name": "Doc 3", "category": "A"})
        
        # Query documents by category
        results = db_handler.query_table("test", "category", "A")
        
        # Check that the correct documents were returned
        assert len(results) == 2
        assert any(doc["name"] == "Doc 1" for doc in results)
        assert any(doc["name"] == "Doc 3" for doc in results)
        assert not any(doc["name"] == "Doc 2" for doc in results)
    
    def test_add_document(self, db_handler):
        """Test adding a document to a table."""
        # Add a test document
        test_data = {"name": "New Document", "value": 456}
        doc_id = db_handler.add_document("test", test_data)
        
        # Check that the document was added
        doc = db_handler.get_document("test", str(doc_id))
        assert doc is not None
        assert doc["name"] == "New Document"
        assert doc["value"] == 456
    
    def test_update_document_existing(self, db_handler):
        """Test updating an existing document."""
        # Add a test document
        test_data = {"name": "Original Document", "value": 789}
        doc_id = db_handler.add_document("test", test_data)
        
        # Update the document
        update_data = {"value": 999, "updated": True}
        result = db_handler.update_document("test", doc_id, update_data)
        
        # Check that the update was successful
        assert result is True
        
        # Check that the document was updated
        doc = db_handler.get_document("test", str(doc_id))
        assert doc is not None
        assert doc["name"] == "Original Document"  # Original field preserved
        assert doc["value"] == 999  # Updated field
        assert doc["updated"] is True  # New field added
    
    def test_update_document_non_existing(self, db_handler):
        """Test updating a non-existing document."""
        # Try to update a document that doesn't exist
        update_data = {"value": 999}
        result = db_handler.update_document("test", 999, update_data)
        
        # Check that the update failed
        assert result is False
    
    def test_delete_document_existing(self, db_handler):
        """Test deleting an existing document."""
        # Add a test document
        test_data = {"name": "Document to Delete"}
        doc_id = db_handler.add_document("test", test_data)
        
        # Delete the document
        result = db_handler.delete_document("test", doc_id)
        
        # Check that the deletion was successful
        assert result is True
        
        # Check that the document was deleted
        doc = db_handler.get_document("test", str(doc_id))
        assert doc is None
    
    def test_delete_document_non_existing(self, db_handler):
        """Test deleting a non-existing document."""
        # Try to delete a document that doesn't exist
        result = db_handler.delete_document("test", 999)
        
        # Check that the deletion failed
        assert result is False
    
    def test_store_lead(self, db_handler):
        """Test storing lead information."""
        # Create lead data
        lead_data = {
            "client_name": "Test Client",
            "client_business": "Test Business",
            "contact_information": "test@example.com",
            "project_description": "Test Project",
            "features": ["Feature 1", "Feature 2"],
            "timeline": "2 months",
            "budget_range": "$5,000-$10,000",
            "confirmed_follow_up": True
        }
        
        # Store the lead
        lead_id = db_handler.store_lead(lead_data)
        
        # Check that the lead was stored
        lead = db_handler.get_document("leads", str(lead_id))
        assert lead is not None
        assert lead["client_name"] == "Test Client"
        assert lead["contact_information"] == "test@example.com"
        assert "timestamp" in lead  # Check that timestamp was added
    
    def test_backup_database(self, db_handler, temp_db_path):
        """Test backing up the database."""
        # Add some data to the database
        db_handler.add_document("test", {"name": "Backup Test"})
        
        # Backup the database
        result = db_handler.backup_database()
        
        # Check that the backup was successful
        assert result["success"] is True
        assert os.path.exists(result["backup_path"])
        
        # Clean up the backup file
        if os.path.exists(result["backup_path"]):
            os.remove(result["backup_path"]) 