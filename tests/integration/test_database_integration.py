"""
Integration tests for TinyDB database integration.

This module contains tests that verify the integration between the application
and the TinyDB database, including real database operations.
"""

import os
import pytest
import tempfile
import datetime
import json
from typing import Dict, List, Any, Optional

# Import the DatabaseHandler class
from app.database_handler import DatabaseHandler

class TestDatabaseIntegration:
    """Integration tests for TinyDB database."""
    
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
    
    def test_database_initialization(self, temp_db_path):
        """Test that the database is properly initialized with default data."""
        # Initialize the database handler
        handler = DatabaseHandler(temp_db_path)
        
        # Check that the database file was created
        assert os.path.exists(temp_db_path)
        
        # Check that the default tables were created
        with open(temp_db_path, 'r') as f:
            db_contents = json.load(f)
            assert 'budget_guidance' in db_contents
            assert 'timeline_guidance' in db_contents
            assert 'leads' in db_contents
    
    def test_lead_storage_and_retrieval(self, db_handler):
        """Test storing and retrieving lead information."""
        # Create lead data
        lead_data = {
            "client_name": "Integration Test Client",
            "client_business": "Integration Test Business",
            "contact_information": "integration@example.com",
            "project_description": "Integration Test Project",
            "features": ["Feature A", "Feature B", "Feature C"],
            "timeline": "3 months",
            "budget_range": "$10,000-$20,000",
            "confirmed_follow_up": True
        }
        
        # Store the lead
        lead_id = db_handler.store_lead(lead_data)
        
        # Retrieve the lead
        lead = db_handler.get_document("leads", str(lead_id))
        
        # Check that the lead was stored and retrieved correctly
        assert lead is not None
        assert lead["client_name"] == "Integration Test Client"
        assert lead["contact_information"] == "integration@example.com"
        assert "timestamp" in lead
        assert len(lead["features"]) == 3
    
    def test_budget_guidance_retrieval(self, db_handler):
        """Test retrieving budget guidance information."""
        # Get all budget guidance data
        budget_data = db_handler.get_table_data("budget_guidance")
        
        # Check that the data was retrieved
        assert len(budget_data) > 0
        
        # Check the structure of the data
        for entry in budget_data:
            assert "project_type" in entry
            assert "min_budget" in entry
            assert "max_budget" in entry
    
    def test_timeline_guidance_retrieval(self, db_handler):
        """Test retrieving timeline guidance information."""
        # Get all timeline guidance data
        timeline_data = db_handler.get_table_data("timeline_guidance")
        
        # Check that the data was retrieved
        assert len(timeline_data) > 0
        
        # Check the structure of the data
        for entry in timeline_data:
            assert "project_type" in entry
            assert "min_timeline" in entry
            assert "max_timeline" in entry
    
    def test_query_by_project_type(self, db_handler):
        """Test querying guidance data by project type."""
        # Get the project types from the budget guidance
        budget_data = db_handler.get_table_data("budget_guidance")
        project_types = [entry["project_type"] for entry in budget_data]
        
        # Choose the first project type for testing
        test_project_type = project_types[0]
        
        # Query budget guidance by project type
        results = db_handler.query_table("budget_guidance", "project_type", test_project_type)
        
        # Check that the query returned the correct data
        assert len(results) == 1
        assert results[0]["project_type"] == test_project_type
    
    def test_database_persistence(self, temp_db_path):
        """Test that data persists in the database between handler instances."""
        # Create a handler and add some data
        handler1 = DatabaseHandler(temp_db_path)
        test_data = {"name": "Persistence Test", "value": "test_value"}
        doc_id = handler1.add_document("test", test_data)
        
        # Create a new handler instance and check that the data is still there
        handler2 = DatabaseHandler(temp_db_path)
        doc = handler2.get_document("test", str(doc_id))
        
        # Check that the data persisted
        assert doc is not None
        assert doc["name"] == "Persistence Test"
        assert doc["value"] == "test_value"
    
    def test_backup_and_restore(self, db_handler, temp_db_path):
        """Test backing up and restoring the database."""
        # Add some test data
        db_handler.add_document("test", {"name": "Backup and Restore Test"})
        
        # Backup the database
        backup_result = db_handler.backup_database()
        assert backup_result["success"] is True
        backup_path = backup_result["backup_path"]
        
        # Check that the backup file exists
        assert os.path.exists(backup_path)
        
        # Create a new database from the backup
        restore_path = temp_db_path + ".restored"
        with open(backup_path, 'r') as src, open(restore_path, 'w') as dst:
            dst.write(src.read())
        
        # Create a handler for the restored database
        restored_handler = DatabaseHandler(restore_path)
        
        # Check that the test data is in the restored database
        test_data = restored_handler.query_table("test", "name", "Backup and Restore Test")
        assert len(test_data) == 1
        
        # Clean up
        if os.path.exists(backup_path):
            os.remove(backup_path)
        if os.path.exists(restore_path):
            os.remove(restore_path)
    
    def test_concurrent_operations(self, db_handler):
        """Test performing multiple operations in sequence."""
        # Add multiple documents
        ids = []
        for i in range(5):
            doc_id = db_handler.add_document("test", {"index": i, "name": f"Concurrent Test {i}"})
            ids.append(doc_id)
        
        # Update some documents
        for i in range(0, 5, 2):  # Update every other document
            db_handler.update_document("test", ids[i], {"updated": True})
        
        # Delete some documents
        db_handler.delete_document("test", ids[1])
        db_handler.delete_document("test", ids[3])
        
        # Get all remaining documents
        docs = db_handler.get_table_data("test")
        
        # Check the results
        assert len(docs) == 3  # 5 added, 2 deleted
        updated_docs = [doc for doc in docs if doc.get("updated") is True]
        assert len(updated_docs) == 3  # Every other document was updated 