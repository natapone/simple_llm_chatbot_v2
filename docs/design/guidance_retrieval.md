# Dynamic Guidance Retrieval Design

## Overview
This document outlines the design for storing and retrieving BUDGET GUIDANCE and TIMELINE GUIDANCE from the Firebase database. Instead of hardcoding these values in the system prompt, we'll store them in the database and provide tools for the LLM to retrieve them when needed.

## Database Structure

We'll add two new collections to our Firebase Firestore database:

```
firestore/
├── leads/
│   └── ...
├── budget_guidance/
│   ├── [project_type_id]/
│   │   ├── project_type: String (e.g., "Basic website")
│   │   ├── min_budget: Number
│   │   ├── max_budget: Number
│   │   └── description: String (optional)
│   └── ...
└── timeline_guidance/
    ├── [project_type_id]/
    │   ├── project_type: String (e.g., "Basic website")
    │   ├── min_timeline: String (e.g., "2 weeks")
    │   ├── max_timeline: String (e.g., "4 weeks")
    │   └── description: String (optional)
    └── ...
```

## Tool-Based Approach

We'll implement tools that the LLM can call when it needs guidance information. This approach allows the LLM to retrieve the most up-to-date guidance data on demand.

### Tool Implementation

```python
def get_budget_guidance(project_type=None):
    """Get budget guidance for a specific project type or all types.
    
    Args:
        project_type (str, optional): The type of project to get guidance for.
            If None, returns guidance for all project types.
            
    Returns:
        list: A list of budget guidance dictionaries.
    """
    firebase_handler = FirebaseHandler(os.getenv('FIREBASE_CREDENTIALS_PATH'))
    
    if project_type:
        # Get guidance for specific project type
        guidance = firebase_handler.query_collection(
            'budget_guidance', 
            field='project_type', 
            operator='==', 
            value=project_type
        )
    else:
        # Get all guidance
        guidance = firebase_handler.get_collection_data('budget_guidance')
    
    return guidance

def get_timeline_guidance(project_type=None):
    """Get timeline guidance for a specific project type or all types.
    
    Args:
        project_type (str, optional): The type of project to get guidance for.
            If None, returns guidance for all project types.
            
    Returns:
        list: A list of timeline guidance dictionaries.
    """
    firebase_handler = FirebaseHandler(os.getenv('FIREBASE_CREDENTIALS_PATH'))
    
    if project_type:
        # Get guidance for specific project type
        guidance = firebase_handler.query_collection(
            'timeline_guidance', 
            field='project_type', 
            operator='==', 
            value=project_type
        )
    else:
        # Get all guidance
        guidance = firebase_handler.get_collection_data('timeline_guidance')
    
    return guidance
```

### Firebase Handler Extension

We'll extend the `FirebaseHandler` class with methods to support retrieving guidance data:

```python
def get_collection_data(self, collection_name):
    """Get all documents from a collection.
    
    Args:
        collection_name (str): The name of the collection to retrieve.
        
    Returns:
        list: A list of dictionaries representing the documents.
    """
    docs = self.db.collection(collection_name).stream()
    return [doc.to_dict() for doc in docs]

def query_collection(self, collection_name, field, operator, value):
    """Query a collection with a filter.
    
    Args:
        collection_name (str): The name of the collection to query.
        field (str): The field to filter on.
        operator (str): The comparison operator (==, >, <, etc.).
        value: The value to compare against.
        
    Returns:
        list: A list of dictionaries representing the filtered documents.
    """
    docs = self.db.collection(collection_name).where(field, operator, value).stream()
    return [doc.to_dict() for doc in docs]
```

## Integration with LangFlow

### 1. Tool Registration in LangFlow

We'll register these tools in LangFlow so the LLM can access them:

```python
# In langflow_handler.py
def register_tools(flow):
    """Register custom tools with the LangFlow pipeline."""
    flow.add_tool(get_budget_guidance)
    flow.add_tool(get_timeline_guidance)
    return flow
```

### 2. Tool Usage in System Prompt

We'll update the system prompt to instruct the LLM to use these tools:

```
4. BUDGET GUIDANCE:
   - When the user asks about budget, use the get_budget_guidance tool to retrieve the latest budget information.
   - If the user mentions a specific project type, pass it as a parameter to get more specific guidance.
   - If no specific project type is mentioned, retrieve all guidance and select the most relevant.
   - Format the budget information in a clear, easy-to-understand way.

5. TIMELINE GUIDANCE:
   - When the user asks about timeline, use the get_timeline_guidance tool to retrieve the latest timeline information.
   - If the user mentions a specific project type, pass it as a parameter to get more specific guidance.
   - If no specific project type is mentioned, retrieve all guidance and select the most relevant.
   - Format the timeline information in a clear, easy-to-understand way.
```

## Data Initialization

We'll need to initialize the guidance collections with default data:

```python
def initialize_guidance_data(firebase_handler):
    """Initialize budget and timeline guidance data if not already present."""
    # Check if data already exists
    budget_data = firebase_handler.get_collection_data('budget_guidance')
    if not budget_data:
        # Initialize budget guidance
        budget_guidance = [
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
        
        for guidance in budget_guidance:
            firebase_handler.db.collection('budget_guidance').add(guidance)
    
    # Check if timeline data already exists
    timeline_data = firebase_handler.get_collection_data('timeline_guidance')
    if not timeline_data:
        # Initialize timeline guidance
        timeline_guidance = [
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
        
        for guidance in timeline_guidance:
            firebase_handler.db.collection('timeline_guidance').add(guidance)
```

## Example Conversation Flow

1. User: "How much would it cost to build an e-commerce website?"
2. LLM recognizes this as a budget question about e-commerce
3. LLM calls `get_budget_guidance("E-commerce site")`
4. Firebase returns the current budget range for e-commerce sites
5. LLM formats and presents this information to the user

## Benefits of This Approach

1. **Dynamic Updates**: Guidance data can be updated in the database without changing code or redeploying
2. **Flexibility**: New project types can be added to the database as services expand
3. **Consistency**: All budget and timeline information comes from a single source of truth
4. **Scalability**: The approach can be extended to other types of guidance data in the future

## Implementation Steps

1. **Update Firebase Structure**:
   - Create the new collections in Firestore
   - Initialize with default guidance values

2. **Extend Firebase Handler**:
   - Add methods to retrieve and query collection data

3. **Implement Guidance Tools**:
   - Create the tool functions for retrieving guidance
   - Register them with LangFlow

4. **Update System Prompt**:
   - Modify instructions to reference the guidance tools
   - Remove hardcoded values from the prompt

5. **Testing**:
   - Test tool calls with various project types
   - Verify the LLM uses the latest guidance data 