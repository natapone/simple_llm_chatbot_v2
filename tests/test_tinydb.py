#!/usr/bin/env python3
"""
Test script for TinyDB implementation in Simple LLM Chatbot v2.

This script tests the basic functionality of the DatabaseHandler class,
including creating, reading, updating, and deleting documents.
"""

import os
import sys
import datetime
import json
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the DatabaseHandler
from app.database_handler import DatabaseHandler

def print_separator(title):
    """Print a separator with a title."""
    print("\n" + "=" * 50)
    print(f" {title} ".center(50, "="))
    print("=" * 50 + "\n")

def main():
    """Run tests for the TinyDB implementation."""
    print_separator("TinyDB Test Script")
    
    # Load environment variables
    load_dotenv()
    
    # Get database path from environment variables or use default
    db_path = os.getenv("TINYDB_PATH", "./data/chatbot_db.json")
    print(f"Using database path: {db_path}")
    
    # Initialize database handler
    try:
        db_handler = DatabaseHandler(db_path)
        print("✅ Database handler initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize database handler: {str(e)}")
        return
    
    # Test 1: Add a test document
    print_separator("Test 1: Add Document")
    test_data = {
        "name": "Test Document",
        "description": "This is a test document for TinyDB",
        "created_at": datetime.datetime.now().isoformat()
    }
    try:
        doc_id = db_handler.add_document("test", test_data)
        print(f"✅ Added test document with ID: {doc_id}")
    except Exception as e:
        print(f"❌ Failed to add test document: {str(e)}")
        return
    
    # Test 2: Retrieve the document
    print_separator("Test 2: Get Document")
    try:
        doc = db_handler.get_document("test", str(doc_id))
        if doc:
            print(f"✅ Retrieved document: {json.dumps(doc, indent=2)}")
        else:
            print("❌ Document not found")
            return
    except Exception as e:
        print(f"❌ Failed to retrieve document: {str(e)}")
        return
    
    # Test 3: Update the document
    print_separator("Test 3: Update Document")
    try:
        update_data = {"updated": True, "update_time": datetime.datetime.now().isoformat()}
        update_success = db_handler.update_document("test", doc_id, update_data)
        if update_success:
            print(f"✅ Document updated successfully")
            # Verify the update
            updated_doc = db_handler.get_document("test", str(doc_id))
            print(f"Updated document: {json.dumps(updated_doc, indent=2)}")
        else:
            print("❌ Document update failed")
            return
    except Exception as e:
        print(f"❌ Failed to update document: {str(e)}")
        return
    
    # Test 4: Query documents
    print_separator("Test 4: Query Documents")
    try:
        # Add another document for querying
        another_doc = {
            "name": "Another Test Document",
            "description": "This is another test document for querying",
            "created_at": datetime.datetime.now().isoformat(),
            "category": "test"
        }
        another_id = db_handler.add_document("test", another_doc)
        print(f"✅ Added another test document with ID: {another_id}")
        
        # Query by name
        results = db_handler.query_table("test", "name", "Another Test Document")
        print(f"✅ Query returned {len(results)} results")
        for result in results:
            print(f"Query result: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"❌ Failed to query documents: {str(e)}")
    
    # Test 5: Get all documents in a table
    print_separator("Test 5: Get All Documents")
    try:
        all_docs = db_handler.get_table_data("test")
        print(f"✅ Retrieved {len(all_docs)} documents from test table")
        for doc in all_docs:
            # In TinyDB, the document ID is not part of the document itself
            # We need to use a different approach to display it
            print(f"Document: {json.dumps(doc, indent=2)}")
    except Exception as e:
        print(f"❌ Failed to retrieve all documents: {str(e)}")
    
    # Test 6: Store a lead
    print_separator("Test 6: Store Lead")
    try:
        lead_data = {
            "client_name": "John Doe",
            "client_business": "Doe Enterprises",
            "contact_information": "john@doeenterprises.com",
            "project_description": "Website redesign with e-commerce functionality",
            "features": ["Responsive design", "E-commerce", "Blog"],
            "timeline": "3 months",
            "budget_range": "$5,000-$10,000",
            "confirmed_follow_up": True
        }
        lead_id = db_handler.store_lead(lead_data)
        print(f"✅ Stored lead with ID: {lead_id}")
        
        # Retrieve the lead
        lead = db_handler.get_document("leads", str(lead_id))
        print(f"Retrieved lead: {json.dumps(lead, indent=2)}")
    except Exception as e:
        print(f"❌ Failed to store lead: {str(e)}")
    
    # Test 7: Check budget guidance data
    print_separator("Test 7: Budget Guidance Data")
    try:
        budget_data = db_handler.get_table_data("budget_guidance")
        print(f"✅ Retrieved {len(budget_data)} budget guidance entries")
        for entry in budget_data:
            print(f"Budget guidance for {entry['project_type']}: ${entry['min_budget']}-${entry['max_budget']}")
    except Exception as e:
        print(f"❌ Failed to retrieve budget guidance: {str(e)}")
    
    # Test 8: Check timeline guidance data
    print_separator("Test 8: Timeline Guidance Data")
    try:
        timeline_data = db_handler.get_table_data("timeline_guidance")
        print(f"✅ Retrieved {len(timeline_data)} timeline guidance entries")
        for entry in timeline_data:
            print(f"Timeline guidance for {entry['project_type']}: {entry['min_timeline']} to {entry['max_timeline']}")
    except Exception as e:
        print(f"❌ Failed to retrieve timeline guidance: {str(e)}")
    
    # Test 9: Delete test documents
    print_separator("Test 9: Delete Documents")
    try:
        # Delete the first test document
        delete_success = db_handler.delete_document("test", doc_id)
        print(f"✅ First document deletion {'successful' if delete_success else 'failed'}")
        
        # Delete the second test document
        delete_success = db_handler.delete_document("test", another_id)
        print(f"✅ Second document deletion {'successful' if delete_success else 'failed'}")
        
        # Verify deletion
        remaining_docs = db_handler.get_table_data("test")
        print(f"Remaining documents in test table: {len(remaining_docs)}")
    except Exception as e:
        print(f"❌ Failed to delete documents: {str(e)}")
    
    # Test 10: Backup database
    print_separator("Test 10: Database Backup")
    try:
        backup_result = db_handler.backup_database()
        if backup_result["success"]:
            print(f"✅ Database backup created at: {backup_result['backup_path']}")
        else:
            print(f"❌ Database backup failed: {backup_result['error']}")
    except Exception as e:
        print(f"❌ Failed to backup database: {str(e)}")
    
    print_separator("Test Summary")
    print("All tests completed. Check the output above for any failures.")
    print(f"Database file location: {db_path}")
    
    # Print the database contents
    try:
        with open(db_path, 'r') as f:
            db_contents = json.load(f)
            print(f"\nDatabase contents:\n{json.dumps(db_contents, indent=2)}")
    except Exception as e:
        print(f"Could not read database file: {str(e)}")

if __name__ == "__main__":
    main() 