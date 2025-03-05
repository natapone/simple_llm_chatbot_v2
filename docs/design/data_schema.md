# Data Schema Design

## Overview

This document outlines the data schema for the pre-sales chatbot application. The application uses TinyDB, a lightweight document-oriented database for Python, to store lead information and conversation history.

## Database Structure

The TinyDB database is organized into tables, with each table containing documents. The database file is stored at `./data/chatbot_db.json`.

```
data/
└── chatbot_db.json
```

## Tables

### 1. Leads Table

The `leads` table stores information about potential clients who interact with the chatbot.

#### Schema

```json
{
  "id": "string",                 // Unique identifier for the lead
  "name": "string",               // Lead's name
  "email": "string",              // Lead's email address
  "phone": "string",              // Lead's phone number (optional)
  "project_details": "string",    // Description of the project
  "project_type": "string",       // Type of project (e.g., e-commerce, corporate, blog)
  "budget_range": "string",       // Budget range for the project
  "timeline": "string",           // Expected timeline for the project
  "created_at": "number",         // Timestamp when the lead was created
  "updated_at": "number",         // Timestamp when the lead was last updated
  "conversation_id": "string"     // Reference to the conversation
}
```

### 2. Conversations Table

The `conversations` table stores the chat history between users and the chatbot.

#### Schema

```json
{
  "id": "string",                 // Unique identifier for the conversation
  "messages": [                   // Array of messages in the conversation
    {
      "id": "string",             // Unique identifier for the message
      "role": "string",           // Role of the sender (user or assistant)
      "content": "string",        // Content of the message
      "timestamp": "number"       // Timestamp when the message was sent
    }
  ],
  "lead_id": "string",            // Reference to the lead (if created)
  "created_at": "number",         // Timestamp when the conversation was created
  "updated_at": "number"          // Timestamp when the conversation was last updated
}
```

### 3. Budget Guidance Table

The `budget_guidance` table stores information about budget ranges for different types of projects.

#### Schema

```json
{
  "project_type": "string",       // Type of project (e.g., e-commerce, corporate, blog)
  "min_budget": "number",         // Minimum budget for the project type
  "max_budget": "number",         // Maximum budget for the project type
  "description": "string"         // Description of what's included in the budget
}
```

### 4. Timeline Guidance Table

The `timeline_guidance` table stores information about timeline estimates for different types of projects.

#### Schema

```json
{
  "project_type": "string",       // Type of project (e.g., e-commerce, corporate, blog)
  "min_timeline": "string",       // Minimum timeline for the project type
  "max_timeline": "string",       // Maximum timeline for the project type
  "description": "string"         // Description of the timeline
}
```

## Database Operations

### Lead Operations

```python
# Add a new lead
def add_lead(lead_data, conversation_id=None):
    leads = db.table('leads')
    lead_id = str(uuid.uuid4())
    
    lead = {
        'id': lead_id,
        'name': lead_data.get('name', ''),
        'email': lead_data.get('email', ''),
        'phone': lead_data.get('phone', ''),
        'project_details': lead_data.get('project_details', ''),
        'project_type': lead_data.get('project_type', ''),
        'budget_range': lead_data.get('budget_range', ''),
        'timeline': lead_data.get('timeline', ''),
        'created_at': time.time(),
        'updated_at': time.time()
    }
    
    if conversation_id:
        lead['conversation_id'] = conversation_id
    
    leads.insert(lead)
    
    # Link lead to conversation if provided
    if conversation_id:
        conversations = db.table('conversations')
        Conversation = Query()
        conversations.update({'lead_id': lead_id}, Conversation.id == conversation_id)
    
    return lead_id

# Get a lead by ID
def get_lead(lead_id):
    leads = db.table('leads')
    Lead = Query()
    result = leads.search(Lead.id == lead_id)
    return result[0] if result else None

# Update a lead
def update_lead(lead_id, lead_data):
    leads = db.table('leads')
    Lead = Query()
    lead = leads.search(Lead.id == lead_id)[0]
    
    for key, value in lead_data.items():
        if key in lead and key not in ['id', 'created_at']:
            lead[key] = value
    
    lead['updated_at'] = time.time()
    
    leads.update(lead, Lead.id == lead_id)
    return lead
```

### Conversation Operations

```python
# Create a new conversation
def create_conversation():
    conversations = db.table('conversations')
    conversation_id = str(uuid.uuid4())
    
    conversation = {
        'id': conversation_id,
        'messages': [],
        'created_at': time.time(),
        'updated_at': time.time()
    }
    
    conversations.insert(conversation)
    return conversation_id

# Get a conversation by ID
def get_conversation(conversation_id):
    conversations = db.table('conversations')
    Conversation = Query()
    result = conversations.search(Conversation.id == conversation_id)
    return result[0] if result else None

# Add a message to a conversation
def add_message(conversation_id, role, content):
    conversations = db.table('conversations')
    Conversation = Query()
    conversation = conversations.search(Conversation.id == conversation_id)[0]
    
    message = {
        'id': str(uuid.uuid4()),
        'role': role,
        'content': content,
        'timestamp': time.time()
    }
    
    conversation['messages'].append(message)
    conversation['updated_at'] = time.time()
    
    conversations.update(conversation, Conversation.id == conversation_id)
    return message['id']
```

### Guidance Operations

```python
# Get budget guidance
def get_budget_guidance(project_type=None):
    budget_guidance = db.table('budget_guidance')
    
    if project_type:
        ProjectType = Query()
        return budget_guidance.search(ProjectType.project_type == project_type)
    else:
        return budget_guidance.all()

# Get timeline guidance
def get_timeline_guidance(project_type=None):
    timeline_guidance = db.table('timeline_guidance')
    
    if project_type:
        ProjectType = Query()
        return timeline_guidance.search(ProjectType.project_type == project_type)
    else:
        return timeline_guidance.all()
```

## Data Initialization

The database is initialized with default guidance data using the following function:

```python
def initialize_database():
    # Ensure the data directory exists
    os.makedirs('./data', exist_ok=True)
    
    # Initialize TinyDB
    db = TinyDB('./data/chatbot_db.json')
    
    # Initialize budget guidance
    budget_guidance = db.table('budget_guidance')
    if len(budget_guidance) == 0:
        budget_guidance.insert_multiple([
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
        ])
    
    # Initialize timeline guidance
    timeline_guidance = db.table('timeline_guidance')
    if len(timeline_guidance) == 0:
        timeline_guidance.insert_multiple([
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
        ])
    
    return db
```

## Data Security

Since TinyDB stores data in a local JSON file, it's important to ensure that:

1. The data directory has appropriate file permissions
2. Regular backups of the database file are made
3. Sensitive information is handled according to data protection regulations

For production use, consider implementing:
- Encryption for sensitive data
- Regular database backups
- Access controls for the database file 