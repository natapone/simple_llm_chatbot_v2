# TinyDB Integration for Data Storage

## Overview
This document outlines how the pre-sales chatbot integrates with TinyDB to store lead information collected during conversations with potential clients, as well as guidance data for budget and timeline information.

## TinyDB Setup

### 1. Database File Location
The TinyDB database is stored as a JSON file on the local filesystem. The path to this file is specified in the `.env` file using the `TINYDB_PATH` variable. By default, this is set to `./data/chatbot_db.json`.

### 2. Directory Structure
Ensure the directory for the database file exists:
```bash
mkdir -p data
```

The database file will be automatically created when the application starts if it doesn't already exist.

## Database Structure

### Tables (Collections)

TinyDB organizes data into "tables" which function similarly to collections in document databases. Our application uses the following tables:

#### Leads Table
The main table for storing lead information:

```json
{
  "leads": {
    "1": {
      "timestamp": "2023-03-04T12:00:00Z",
      "client_name": "John Doe",
      "client_business": "Example Business",
      "contact_information": "john@example.com",
      "project_description": "E-commerce website",
      "features": ["Product listing", "Shopping cart", "Payment integration"],
      "timeline": "2 months",
      "budget_range": "$5,000",
      "confirmed_follow_up": true
    },
    "2": {
      // Another lead entry
    }
  }
}
```

#### Budget Guidance Table
Stores budget guidance information for different project types:

```json
{
  "budget_guidance": {
    "1": {
      "project_type": "e-commerce",
      "min_budget": 5000,
      "max_budget": 15000,
      "description": "Basic e-commerce website with product listings and payment processing"
    },
    "2": {
      "project_type": "corporate",
      "min_budget": 3000,
      "max_budget": 10000,
      "description": "Professional corporate website with company information and contact forms"
    }
  }
}
```

#### Timeline Guidance Table
Stores timeline guidance information for different project types:

```json
{
  "timeline_guidance": {
    "1": {
      "project_type": "e-commerce",
      "min_timeline": "6 weeks",
      "max_timeline": "3 months",
      "description": "Development timeline for a standard e-commerce website"
    },
    "2": {
      "project_type": "corporate",
      "min_timeline": "4 weeks",
      "max_timeline": "2 months",
      "description": "Development timeline for a corporate website"
    }
  }
}
```

## Integration Code

### Database Handler

The `database_handler.py` file will contain the code for interacting with TinyDB:

```python
from tinydb import TinyDB, Query
import os
import datetime
from typing import Dict, List, Any, Optional, Union

class DatabaseHandler:
    def __init__(self, db_path: str):
        """Initialize TinyDB connection.
        
        Args:
            db_path: Path to the TinyDB JSON file.
        """
        # Ensure directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db = TinyDB(db_path)
        self.leads_table = self.db.table('leads')
        self.budget_guidance_table = self.db.table('budget_guidance')
        self.timeline_guidance_table = self.db.table('timeline_guidance')
        
    def get_document(self, table_name: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a document by ID from a specific table.
        
        Args:
            table_name: Name of the table to query
            doc_id: ID of the document to retrieve
            
        Returns:
            The document if found, None otherwise
        """
        table = self.db.table(table_name)
        doc = table.get(doc_id=int(doc_id) if doc_id.isdigit() else doc_id)
        return doc
    
    def get_table_data(self, table_name: str) -> List[Dict[str, Any]]:
        """Get all documents from a specific table.
        
        Args:
            table_name: Name of the table to query
            
        Returns:
            List of all documents in the table
        """
        table = self.db.table(table_name)
        return table.all()
    
    def query_table(self, table_name: str, field: str, value: Any) -> List[Dict[str, Any]]:
        """Query a table for documents where field equals value.
        
        Args:
            table_name: Name of the table to query
            field: Field to query on
            value: Value to match
            
        Returns:
            List of matching documents
        """
        table = self.db.table(table_name)
        User = Query()
        return table.search(getattr(User, field) == value)
    
    def add_document(self, table_name: str, data: Dict[str, Any]) -> int:
        """Add a document to a specific table.
        
        Args:
            table_name: Name of the table to add to
            data: Document data to add
            
        Returns:
            ID of the inserted document
        """
        table = self.db.table(table_name)
        return table.insert(data)
    
    def update_document(self, table_name: str, doc_id: Union[str, int], data: Dict[str, Any]) -> bool:
        """Update a document in a specific table.
        
        Args:
            table_name: Name of the table to update
            doc_id: ID of the document to update
            data: New data for the document
            
        Returns:
            True if successful, False otherwise
        """
        table = self.db.table(table_name)
        doc_id = int(doc_id) if isinstance(doc_id, str) and doc_id.isdigit() else doc_id
        return table.update(data, doc_ids=[doc_id]) > 0
    
    def delete_document(self, table_name: str, doc_id: Union[str, int]) -> bool:
        """Delete a document from a specific table.
        
        Args:
            table_name: Name of the table to delete from
            doc_id: ID of the document to delete
            
        Returns:
            True if successful, False otherwise
        """
        table = self.db.table(table_name)
        doc_id = int(doc_id) if isinstance(doc_id, str) and doc_id.isdigit() else doc_id
        return table.remove(doc_ids=[doc_id]) > 0
    
    def store_lead(self, lead_data: Dict[str, Any]) -> int:
        """Store lead information in the leads table.
        
        Args:
            lead_data: Dictionary containing lead information
                - client_name: Name of the client
                - client_business: Client's business name
                - contact_information: Email or phone
                - project_description: Description of the project
                - features: List of desired features
                - timeline: Expected timeline
                - budget_range: Budget range
                - confirmed_follow_up: Whether follow-up is confirmed
                
        Returns:
            ID of the created lead document
        """
        # Add timestamp
        lead_data['timestamp'] = datetime.datetime.now().isoformat()
        
        # Store in TinyDB
        return self.leads_table.insert(lead_data)
```

## Integration with LangFlow

### 1. Custom Node in LangFlow
Create a custom node in LangFlow that:
1. Receives lead information from the conversation
2. Validates that all required fields are present
3. Calls the database handler to store the lead
4. Returns a success/failure message

### 2. Decision Logic
Implement logic in the LangFlow pipeline to determine when to store lead information:
1. Check if all required fields are collected
2. Verify that the user has given consent for follow-up
3. Only then trigger the database storage node

## Data Persistence

TinyDB stores all data in a single JSON file, which provides several benefits:

1. **Simplicity**: No need for a separate database server
2. **Portability**: The database can be easily backed up or moved
3. **Human-readable**: The database can be inspected and edited with a text editor
4. **Version control**: The database file can be included in version control (though this is not recommended for production data)

## Initialization

When the application starts, it will:

1. Check if the database file exists
2. Create it if it doesn't
3. Initialize default data for budget and timeline guidance if those tables are empty

## Testing the Integration

### 1. Manual Testing
1. Run a test conversation with the chatbot
2. Provide all required information and consent for follow-up
3. Check the database file to verify the lead was stored correctly

### 2. Automated Testing
Create test cases for:
1. Successful lead storage
2. Handling missing fields
3. Error handling for database operations

## Future Enhancements

1. **Data Export**: Add functionality to export leads as CSV or other formats
2. **Data Backup**: Implement automatic backups of the database file
3. **Migration to SQL**: If data volume grows, provide migration path to SQLite or PostgreSQL
4. **Admin Interface**: Create a simple admin interface for managing leads and guidance data
5. **Data Validation**: Add more robust validation for data before storage 