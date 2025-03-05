# Dynamic Guidance Retrieval Design

## Overview
This document outlines the design for storing and retrieving BUDGET GUIDANCE and TIMELINE GUIDANCE from the TinyDB database. Instead of hardcoding these values in the system prompt, we'll store them in the database and provide tools for the LLM to retrieve them when needed.

## Database Structure

We'll add two tables to our TinyDB database:

### 1. Budget Guidance Table
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
    },
    "3": {
      "project_type": "blog",
      "min_budget": 2000,
      "max_budget": 5000,
      "description": "Blog website with content management system"
    }
  }
}
```

### 2. Timeline Guidance Table
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
    },
    "3": {
      "project_type": "blog",
      "min_timeline": "2 weeks",
      "max_timeline": "1 month",
      "description": "Development timeline for a blog website"
    }
  }
}
```

## Guidance Retrieval Tools

We'll create two Python functions that the LLM can call to retrieve guidance:

### 1. Budget Guidance Tool

```python
def get_budget_guidance(project_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieve budget guidance from the database.
    
    Args:
        project_type: Optional project type to filter by (e.g., "e-commerce", "corporate", "blog")
        
    Returns:
        List of budget guidance entries
    """
    db_handler = DatabaseHandler(os.getenv('TINYDB_PATH'))
    
    if project_type:
        # Query for specific project type
        guidance = db_handler.query_table(
            'budget_guidance', 
            'project_type', 
            project_type
        )
    else:
        # Get all guidance
        guidance = db_handler.get_table_data('budget_guidance')
    
    return guidance
```

### 2. Timeline Guidance Tool

```python
def get_timeline_guidance(project_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieve timeline guidance from the database.
    
    Args:
        project_type: Optional project type to filter by (e.g., "e-commerce", "corporate", "blog")
        
    Returns:
        List of timeline guidance entries
    """
    db_handler = DatabaseHandler(os.getenv('TINYDB_PATH'))
    
    if project_type:
        # Query for specific project type
        guidance = db_handler.query_table(
            'timeline_guidance', 
            'project_type', 
            project_type
        )
    else:
        # Get all guidance
        guidance = db_handler.get_table_data('timeline_guidance')
    
    return guidance
```

### DatabaseHandler Extension

We'll extend the `DatabaseHandler` class with methods to support retrieving guidance data:

```python
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

def get_table_data(self, table_name: str) -> List[Dict[str, Any]]:
    """Get all documents from a specific table.
    
    Args:
        table_name: Name of the table to query
        
    Returns:
        List of all documents in the table
    """
    table = self.db.table(table_name)
    return table.all()
```

## Formatting Functions

We'll also create functions to format the guidance data in a user-friendly way:

```python
def format_budget_guidance(guidance: List[Dict[str, Any]]) -> str:
    """Format budget guidance data for display to the user.
    
    Args:
        guidance: List of budget guidance entries
        
    Returns:
        Formatted string with budget guidance
    """
    if not guidance:
        return "I don't have specific budget guidance for that project type. " \
               "Please let me know what kind of website you're interested in, and I can provide more information."
    
    result = "Based on our experience, here's the budget guidance for your project:\n\n"
    
    for item in guidance:
        result += f"- {item['project_type'].title()} Website: ${item['min_budget']:,} to ${item['max_budget']:,}\n"
        if 'description' in item:
            result += f"  {item['description']}\n"
        result += "\n"
    
    return result

def format_timeline_guidance(guidance: List[Dict[str, Any]]) -> str:
    """Format timeline guidance data for display to the user.
    
    Args:
        guidance: List of timeline guidance entries
        
    Returns:
        Formatted string with timeline guidance
    """
    if not guidance:
        return "I don't have specific timeline guidance for that project type. " \
               "Please let me know what kind of website you're interested in, and I can provide more information."
    
    result = "Based on our experience, here's the timeline guidance for your project:\n\n"
    
    for item in guidance:
        result += f"- {item['project_type'].title()} Website: {item['min_timeline']} to {item['max_timeline']}\n"
        if 'description' in item:
            result += f"  {item['description']}\n"
        result += "\n"
    
    return result
```

## Initialization Function

We'll create a function to initialize the guidance data in the database:

```python
def initialize_guidance_data(db_handler):
    """Initialize guidance data in the database if it doesn't exist.
    
    Args:
        db_handler: DatabaseHandler instance
    """
    # Check if budget guidance exists
    budget_data = db_handler.get_table_data('budget_guidance')
    
    if not budget_data:
        # Add default budget guidance
        budget_guidance = [
            {
                "project_type": "e-commerce",
                "min_budget": 5000,
                "max_budget": 15000,
                "description": "Basic e-commerce website with product listings and payment processing"
            },
            {
                "project_type": "corporate",
                "min_budget": 3000,
                "max_budget": 10000,
                "description": "Professional corporate website with company information and contact forms"
            },
            {
                "project_type": "blog",
                "min_budget": 2000,
                "max_budget": 5000,
                "description": "Blog website with content management system"
            }
        ]
        
        for guidance in budget_guidance:
            db_handler.add_document('budget_guidance', guidance)
    
    # Check if timeline guidance exists
    timeline_data = db_handler.get_table_data('timeline_guidance')
    
    if not timeline_data:
        # Add default timeline guidance
        timeline_guidance = [
            {
                "project_type": "e-commerce",
                "min_timeline": "6 weeks",
                "max_timeline": "3 months",
                "description": "Development timeline for a standard e-commerce website"
            },
            {
                "project_type": "corporate",
                "min_timeline": "4 weeks",
                "max_timeline": "2 months",
                "description": "Development timeline for a corporate website"
            },
            {
                "project_type": "blog",
                "min_timeline": "2 weeks",
                "max_timeline": "1 month",
                "description": "Development timeline for a blog website"
            }
        ]
        
        for guidance in timeline_guidance:
            db_handler.add_document('timeline_guidance', guidance)
```

## Example Usage

### Budget Guidance Example

1. User asks: "How much would an e-commerce website cost?"
2. LLM detects this is a budget question about e-commerce
3. LLM calls `get_budget_guidance("e-commerce")`
4. TinyDB returns the current budget range for e-commerce sites
5. LLM formats and presents this information to the user

### Timeline Guidance Example

1. User asks: "How long would it take to build a corporate website?"
2. LLM detects this is a timeline question about corporate websites
3. LLM calls `get_timeline_guidance("corporate")`
4. TinyDB returns the current timeline range for corporate sites
5. LLM formats and presents this information to the user

## Implementation Steps

1. **Update TinyDB Structure**:
   - Create the budget_guidance and timeline_guidance tables
   - Add initial data to these tables

2. **Extend DatabaseHandler**:
   - Add methods for querying tables
   - Add methods for retrieving all data from a table

3. **Create Guidance Tools**:
   - Implement get_budget_guidance function
   - Implement get_timeline_guidance function
   - Implement formatting functions

4. **Update LangFlow Pipeline**:
   - Register the guidance tools with the LLM
   - Update the system prompt to instruct the LLM to use these tools

5. **Test the Implementation**:
   - Test with various user queries about budget and timeline
   - Verify that the LLM correctly retrieves and presents the guidance 