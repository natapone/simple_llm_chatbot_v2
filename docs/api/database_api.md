# Database API Documentation

## Overview

This document outlines the API for interacting with the TinyDB database in the Simple LLM Chatbot v2 project. The database stores lead information, budget guidance, and timeline guidance data.

## DatabaseHandler Class

The `DatabaseHandler` class provides methods for interacting with the TinyDB database. It is located in the `database_handler.py` file.

### Initialization

```python
from database_handler import DatabaseHandler

# Initialize the database handler
db_handler = DatabaseHandler(db_path="./data/chatbot_db.json")
```

### Methods

#### Get Document

Retrieves a document by ID from a specific table.

```python
document = db_handler.get_document(table_name="leads", doc_id="1")
```

**Parameters:**
- `table_name` (str): Name of the table to query
- `doc_id` (str): ID of the document to retrieve

**Returns:**
- `dict` or `None`: The document if found, None otherwise

#### Get Table Data

Retrieves all documents from a specific table.

```python
all_leads = db_handler.get_table_data(table_name="leads")
```

**Parameters:**
- `table_name` (str): Name of the table to query

**Returns:**
- `list`: List of all documents in the table

#### Query Table

Queries a table for documents where a field equals a specific value.

```python
# Find leads with a specific client name
matching_leads = db_handler.query_table(
    table_name="leads", 
    field="client_name", 
    value="John Doe"
)
```

**Parameters:**
- `table_name` (str): Name of the table to query
- `field` (str): Field to query on
- `value` (Any): Value to match

**Returns:**
- `list`: List of matching documents

#### Add Document

Adds a document to a specific table.

```python
# Add a new budget guidance entry
doc_id = db_handler.add_document(
    table_name="budget_guidance",
    data={
        "project_type": "mobile_app",
        "min_budget": 8000,
        "max_budget": 20000,
        "description": "Native mobile application development"
    }
)
```

**Parameters:**
- `table_name` (str): Name of the table to add to
- `data` (dict): Document data to add

**Returns:**
- `int`: ID of the inserted document

#### Update Document

Updates a document in a specific table.

```python
# Update a lead's contact information
success = db_handler.update_document(
    table_name="leads",
    doc_id="1",
    data={"contact_information": "updated_email@example.com"}
)
```

**Parameters:**
- `table_name` (str): Name of the table to update
- `doc_id` (str or int): ID of the document to update
- `data` (dict): New data for the document

**Returns:**
- `bool`: True if successful, False otherwise

#### Delete Document

Deletes a document from a specific table.

```python
# Delete a lead
success = db_handler.delete_document(table_name="leads", doc_id="1")
```

**Parameters:**
- `table_name` (str): Name of the table to delete from
- `doc_id` (str or int): ID of the document to delete

**Returns:**
- `bool`: True if successful, False otherwise

#### Store Lead

Stores lead information in the leads table.

```python
# Store a new lead
lead_id = db_handler.store_lead({
    "client_name": "Jane Smith",
    "client_business": "Smith Enterprises",
    "contact_information": "jane@smithenterprises.com",
    "project_description": "Corporate website redesign",
    "features": ["Responsive design", "Content management system", "Contact form"],
    "timeline": "3 months",
    "budget_range": "$8,000-$12,000",
    "confirmed_follow_up": True
})
```

**Parameters:**
- `lead_data` (dict): Dictionary containing lead information
  - `client_name` (str): Name of the client
  - `client_business` (str): Client's business name
  - `contact_information` (str): Email or phone
  - `project_description` (str): Description of the project
  - `features` (list): List of desired features
  - `timeline` (str): Expected timeline
  - `budget_range` (str): Budget range
  - `confirmed_follow_up` (bool): Whether follow-up is confirmed

**Returns:**
- `int`: ID of the created lead document

## Usage Examples

### Initializing the Database

```python
import os
from dotenv import load_dotenv
from database_handler import DatabaseHandler

# Load environment variables
load_dotenv()

# Get database path from environment variables
db_path = os.getenv("TINYDB_PATH", "./data/chatbot_db.json")

# Initialize database handler
db_handler = DatabaseHandler(db_path)
```

### Storing a Lead

```python
def process_lead_information(lead_info):
    """Process and store lead information."""
    # Validate lead information
    required_fields = [
        "client_name", "client_business", "contact_information",
        "project_description", "confirmed_follow_up"
    ]
    
    for field in required_fields:
        if field not in lead_info:
            return {"success": False, "error": f"Missing required field: {field}"}
    
    # Store lead in database
    try:
        lead_id = db_handler.store_lead(lead_info)
        return {"success": True, "lead_id": lead_id}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### Retrieving Budget Guidance

```python
def get_budget_guidance(project_type):
    """Get budget guidance for a specific project type."""
    # Query the budget guidance table
    guidance_entries = db_handler.query_table(
        table_name="budget_guidance",
        field="project_type",
        value=project_type.lower()
    )
    
    if not guidance_entries:
        # Return default guidance if no specific entry is found
        return {
            "min_budget": 5000,
            "max_budget": 15000,
            "description": "Standard web development project"
        }
    
    return guidance_entries[0]
```

### Retrieving Timeline Guidance

```python
def get_timeline_guidance(project_type):
    """Get timeline guidance for a specific project type."""
    # Query the timeline guidance table
    guidance_entries = db_handler.query_table(
        table_name="timeline_guidance",
        field="project_type",
        value=project_type.lower()
    )
    
    if not guidance_entries:
        # Return default guidance if no specific entry is found
        return {
            "min_timeline": "4 weeks",
            "max_timeline": "3 months",
            "description": "Standard web development timeline"
        }
    
    return guidance_entries[0]
```

## Error Handling

The database handler includes error handling for common issues:

1. **File Not Found**: If the database file doesn't exist, it will be created automatically.
2. **Permission Errors**: If there are permission issues with the database file, an exception will be raised.
3. **Invalid Document ID**: If an invalid document ID is provided, the operation will fail gracefully.
4. **Invalid Table Name**: If an invalid table name is provided, a new table will be created.

Example error handling:

```python
try:
    document = db_handler.get_document(table_name="leads", doc_id="invalid_id")
    if document is None:
        print("Document not found")
    else:
        print(f"Found document: {document}")
except Exception as e:
    print(f"Error accessing database: {str(e)}")
```

## Data Backup

It's recommended to regularly back up the TinyDB database file. A simple backup function:

```python
import shutil
import datetime

def backup_database(db_path):
    """Create a backup of the database file."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{db_path}.backup_{timestamp}"
    
    try:
        shutil.copy2(db_path, backup_path)
        return {"success": True, "backup_path": backup_path}
    except Exception as e:
        return {"success": False, "error": str(e)}
``` 