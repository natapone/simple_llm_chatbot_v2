# LangFlow Pipeline Design for Pre-Sales Chatbot

## Overview
This document outlines the design of the LangFlow pipeline for the pre-sales chatbot. The pipeline orchestrates the conversation flow, retrieves guidance information, and triggers lead storage in TinyDB. This design incorporates the conversation flow and data schema defined in their respective design documents.

## Pipeline Components

The pipeline consists of the following components:

### 1. System Prompt Node
- **Type**: SystemMessagePromptTemplate
- **Parameters**:
  - `prompt`: The system prompt that guides the chatbot's behavior

### 2. Human Message Node
- **Type**: HumanMessagePromptTemplate
- **Parameters**:
  - `prompt`: The user's message

### 3. Chat History Node
- **Type**: ConversationBufferMemory
- **Parameters**:
  - `memory_key`: "chat_history"
  - `return_messages`: true

### 4. LiteLLM Node
- **Type**: LiteLLMNode
- **Parameters**:
  - `model`: The language model to use (e.g., "gpt-4", "claude-2")
  - `temperature`: 0.7
  - `max_tokens`: 800

### 5. Budget Guidance Tool Node
- **Type**: PythonFunctionNode
- **Parameters**:
  - `function`: get_budget_guidance
  - `project_type`: Project type detected from conversation

### 6. Timeline Guidance Tool Node
- **Type**: PythonFunctionNode
- **Parameters**:
  - `function`: get_timeline_guidance
  - `project_type`: Project type detected from conversation

### 7. Project Type Detection Node
- **Type**: PythonFunctionNode
- **Parameters**:
  - `function`: detect_project_type
  - `conversation_history`: The conversation history

### 8. Lead Extraction Node
- **Type**: PythonFunctionNode
- **Parameters**:
  - `function`: extract_lead_information
  - `conversation_history`: The conversation history

### 9. TinyDB Storage Node
- **Type**: PythonFunctionNode
- **Parameters**:
  - `function`: store_lead
  - `lead_data`: The extracted lead information
  - `db_path`: Path to TinyDB database

### 10. Conversation Storage Node
- **Type**: PythonFunctionNode
- **Parameters**:
  - `function`: store_conversation
  - `conversation_history`: The conversation history
  - `db_path`: Path to TinyDB database

## Pipeline Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │
│  System     │────►│  Human      │────►│  Chat       │
│  Prompt     │     │  Message    │     │  History    │
│             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
       │                                       │
       │                                       │
       │                                       ▼
       │                                ┌─────────────┐
       │                                │             │
       └───────────────────────────────►│  LiteLLM    │
                                        │             │
                                        └─────────────┘
                                               │
                                               │
                                               ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │
│  Project    │────►│  Budget     │────►│  Timeline   │
│  Type       │     │  Guidance   │     │  Guidance   │
│             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
       │                                       │
       │                                       │
       ▼                                       │
┌─────────────┐                                │
│             │                                │
│  Lead       │◄───────────────────────────────┘
│  Extraction │
│             │
└─────────────┘
       │
       │
       ▼
┌─────────────┐     ┌─────────────┐
│             │     │             │
│  TinyDB     │────►│  Conversation│
│  Storage    │     │  Storage    │
│             │     │             │
└─────────────┘     └─────────────┘
```

## Node Implementations

### 1. System Prompt Node

The system prompt node provides the initial instructions to the LLM about its role and behavior. The prompt is defined in the [System Prompt Design](system_prompt.md) document.

```python
system_prompt = """
You are a friendly and helpful pre-sales chatbot for a software development company. Your goal is to engage with potential clients, understand their project needs, and collect their contact information for follow-up.

Follow these guidelines in your conversation:

1. CONVERSATION FLOW:
   - Start by greeting the user and asking about their business needs.
   - Explore their project requirements and desired features.
   - Ask about their timeline expectations.
   - Discuss budget considerations.
   - Collect their contact information.
   - Confirm consent for follow-up.
   - Close the conversation with a thank you message.

2. TONE AND STYLE:
   - Be friendly, professional, and helpful.
   - Use simple language, avoiding technical jargon unless the user demonstrates technical knowledge.
   - Ask one question at a time to keep the conversation natural.
   - Be concise in your responses.

3. LEAD INFORMATION COLLECTION:
   - Collect the following information throughout the conversation:
     * Client name
     * Client business/company
     * Project description
     * Desired features
     * Timeline expectations
     * Budget range
     * Contact information (email or phone)
     * Consent for follow-up

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

6. CONTACT INFORMATION:
   - Ask for contact information (name and email) only after understanding their project needs.
   - Always ask for explicit consent before storing their information for follow-up.
   - If they decline to provide contact information or do not consent to follow-up, thank them for their time and end the conversation politely.

7. LEAD STORAGE CRITERIA:
   - Only trigger lead storage in the database when ALL of the following conditions are met:
     * You have collected their name
     * You have collected their contact information (email or phone)
     * You have received explicit consent for follow-up
     * You have basic information about their project needs

8. HANDLING UNCERTAINTY:
   - If the user is vague or uncertain, provide examples to help guide them.
   - If you don't understand a request, politely ask for clarification.
   - If the user asks questions outside your scope, explain that you're focused on understanding their software development needs.
"""
```

### 2. Human Message Node

The human message node represents the user's input to the conversation.

```python
human_message = "{input}"
```

### 3. Chat History Node

The chat history node maintains the conversation context.

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="output",
    input_key="input",
    human_prefix="User",
    ai_prefix="Assistant"
)
```

### 4. LiteLLM Node

The LiteLLM node handles the interaction with the language model.

```python
import os
import litellm

def generate_response(messages, model="gpt-4", temperature=0.7, max_tokens=800):
    """Generate a response using LiteLLM.
    
    Args:
        messages: List of message objects
        model: The model to use
        temperature: Temperature parameter for generation
        max_tokens: Maximum number of tokens to generate
        
    Returns:
        The generated response
    """
    response = litellm.completion(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=api_key  # Explicitly pass the API key
    )
    
    return response.choices[0].message.content
```

### 5. Budget Guidance Tool Node

The budget guidance tool retrieves budget information from TinyDB based on the project type.

```python
import os
from typing import List, Dict, Any, Optional
from database_handler import DatabaseHandler

def get_budget_guidance(project_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get budget guidance for a specific project type or all types.
    
    Args:
        project_type: The type of project to get guidance for.
            If None, returns guidance for all project types.
            
    Returns:
        A list of budget guidance dictionaries.
    """
    db_handler = DatabaseHandler(os.getenv('TINYDB_PATH'))
    
    if project_type:
        # Get guidance for specific project type
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

### 6. Timeline Guidance Tool Node

The timeline guidance tool retrieves timeline information from TinyDB based on the project type.

```python
import os
from typing import List, Dict, Any, Optional
from database_handler import DatabaseHandler

def get_timeline_guidance(project_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get timeline guidance for a specific project type or all types.
    
    Args:
        project_type: The type of project to get guidance for.
            If None, returns guidance for all project types.
            
    Returns:
        A list of timeline guidance dictionaries.
    """
    db_handler = DatabaseHandler(os.getenv('TINYDB_PATH'))
    
    if project_type:
        # Get guidance for specific project type
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

### 7. Project Type Detection Node

The project type detection node analyzes the conversation to determine the type of project the user is interested in.

```python
from typing import List, Dict, Any, Optional

def detect_project_type(conversation_history: List[Dict[str, Any]], standard_project_types: List[str]) -> Optional[str]:
    """Detect the project type from the conversation history.
    
    Args:
        conversation_history: The conversation history
        standard_project_types: List of standard project types
        
    Returns:
        The detected project type or None if no project type is detected
    """
    # Convert conversation history to a single string for analysis
    conversation_text = " ".join([msg["content"] for msg in conversation_history])
    conversation_text = conversation_text.lower()
    
    # Check for standard project types
    for project_type in standard_project_types:
        if project_type.lower() in conversation_text:
            return project_type
    
    # Check for specific keywords
    if any(keyword in conversation_text for keyword in ["shop", "store", "product", "cart", "checkout", "payment"]):
        return "e-commerce"
    
    if any(keyword in conversation_text for keyword in ["company", "business", "corporate", "professional", "organization"]):
        return "corporate"
    
    if any(keyword in conversation_text for keyword in ["blog", "content", "article", "post", "cms"]):
        return "blog"
    
    # No project type detected
    return None
```

### 8. Lead Extraction Node

The lead extraction node analyzes the conversation to extract lead information.

```python
from typing import List, Dict, Any, Optional
import re

def extract_lead_information(conversation_history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Extract lead information from the conversation history.
    
    Args:
        conversation_history: The conversation history
        
    Returns:
        A dictionary containing the extracted lead information
    """
    # Convert conversation history to a single string for analysis
    conversation_text = " ".join([msg["content"] for msg in conversation_history])
    
    # Initialize lead data
    lead_data = {
        "client_name": None,
        "client_business": None,
        "contact_information": None,
        "project_description": None,
        "features": [],
        "timeline": None,
        "budget_range": None,
        "confirmed_follow_up": False,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    # Extract client name
    name_patterns = [
        r"my name is ([A-Za-z\s]+)",
        r"I'm ([A-Za-z\s]+)",
        r"I am ([A-Za-z\s]+)",
        r"([A-Za-z\s]+) here"
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, conversation_text, re.IGNORECASE)
        if match:
            lead_data["client_name"] = match.group(1).strip()
            break
    
    # Extract contact information (email)
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_matches = re.findall(email_pattern, conversation_text)
    if email_matches:
        lead_data["contact_information"] = email_matches[0]
    
    # Extract project description
    project_patterns = [
        r"I need ([^.]+)",
        r"I want ([^.]+)",
        r"I'm looking for ([^.]+)",
        r"I am looking for ([^.]+)"
    ]
    
    for pattern in project_patterns:
        match = re.search(pattern, conversation_text, re.IGNORECASE)
        if match:
            lead_data["project_description"] = match.group(1).strip()
            break
    
    # Extract budget range
    budget_patterns = [
        r"budget is (\$?[\d,]+\s*-\s*\$?[\d,]+)",
        r"budget of (\$?[\d,]+\s*-\s*\$?[\d,]+)",
        r"(\$?[\d,]+\s*-\s*\$?[\d,]+) budget",
        r"around (\$?[\d,]+)"
    ]
    
    for pattern in budget_patterns:
        match = re.search(pattern, conversation_text, re.IGNORECASE)
        if match:
            lead_data["budget_range"] = match.group(1).strip()
            break
    
    # Extract timeline
    timeline_patterns = [
        r"timeline is ([\w\s]+)",
        r"timeline of ([\w\s]+)",
        r"within ([\w\s]+)",
        r"([\d]+ weeks)",
        r"([\d]+ months)"
    ]
    
    for pattern in timeline_patterns:
        match = re.search(pattern, conversation_text, re.IGNORECASE)
        if match:
            lead_data["timeline"] = match.group(1).strip()
            break
    
    # Extract features
    feature_patterns = [
        r"features like ([\w\s,]+)",
        r"features such as ([\w\s,]+)",
        r"need ([\w\s,]+) features",
        r"want ([\w\s,]+) features"
    ]
    
    for pattern in feature_patterns:
        match = re.search(pattern, conversation_text, re.IGNORECASE)
        if match:
            features_text = match.group(1).strip()
            features = [f.strip() for f in features_text.split(",")]
            lead_data["features"].extend(features)
            break
    
    # Check for follow-up consent
    consent_patterns = [
        r"yes, you can contact me",
        r"yes, you can email me",
        r"yes, you can reach out",
        r"that's fine",
        r"that is fine",
        r"sure, you can",
        r"yes, that's fine",
        r"yes, that is fine"
    ]
    
    for pattern in consent_patterns:
        if re.search(pattern, conversation_text, re.IGNORECASE):
            lead_data["confirmed_follow_up"] = True
            break
    
    # Clean up None values
    lead_data = {k: v for k, v in lead_data.items() if v is not None and v != [] and v != ""}
    
    return lead_data
```

### 9. TinyDB Storage Node (Leads)

The TinyDB storage node stores lead information in the TinyDB database.

```python
import os
import datetime
from typing import Dict, Any, Optional
from database_handler import DatabaseHandler

def store_lead(lead_data: Dict[str, Any], db_path: Optional[str] = None) -> str:
    """Store lead information in TinyDB.
    
    Args:
        lead_data: The lead information to store
        db_path: Path to TinyDB database
        
    Returns:
        The ID of the stored lead
    """
    # Use provided db_path or get from environment
    if not db_path:
        db_path = os.getenv('TINYDB_PATH')
    
    # Create TinyDB handler
    db_handler = DatabaseHandler(db_path)
    
    # Validate lead data
    required_fields = ["client_name", "contact_information", "confirmed_follow_up"]
    for field in required_fields:
        if field not in lead_data or not lead_data[field]:
            return None
    
    # Only store if consent is given
    if not lead_data.get("confirmed_follow_up", False):
        return None
    
    # Add timestamp if not present
    if "timestamp" not in lead_data:
        lead_data["timestamp"] = datetime.datetime.now().isoformat()
    
    # Store lead in database
    lead_id = db_handler.add_document("leads", lead_data)
    
    return lead_id
```

### 10. Conversation Storage Node

The conversation storage node stores the conversation history in the TinyDB database.

```python
import os
import datetime
from typing import List, Dict, Any, Optional
from database_handler import DatabaseHandler

def store_conversation(conversation_history: List[Dict[str, Any]], db_path: Optional[str] = None) -> str:
    """Store conversation history in TinyDB.
    
    Args:
        conversation_history: The conversation history to store
        db_path: Path to TinyDB database
        
    Returns:
        The ID of the stored conversation
    """
    # Use provided db_path or get from environment
    if not db_path:
        db_path = os.getenv('TINYDB_PATH')
    
    # Create TinyDB handler
    db_handler = DatabaseHandler(db_path)
    
    # Create conversation data
    conversation_data = {
        "messages": conversation_history,
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat(),
        "message_count": len(conversation_history)
    }
    
    # Store conversation in database
    conversation_id = db_handler.add_document("conversations", conversation_data)
    
    return conversation_id
```

## Enhanced Tool Logic

### Enhanced Lead Extraction Logic

```python
def extract_lead_information(conversation_history):
    """Extract lead information from the conversation history.
    
    This function analyzes the conversation history to extract information about the potential client,
    including their name, contact information, project details, budget, and timeline.
    
    Args:
        conversation_history: List of message objects representing the conversation
        
    Returns:
        Dictionary containing the extracted lead information
    """
    # Implementation details as shown in the Lead Extraction Node section
    pass
```

### Enhanced TinyDB Storage Logic

```python
def store_lead(lead_data, db_path=None):
    """Store lead information in TinyDB.
    
    This function validates the lead data and stores it in the TinyDB database if all required
    fields are present and the user has given consent for follow-up.
    
    Args:
        lead_data: Dictionary containing lead information
        db_path: Path to TinyDB database
        
    Returns:
        The ID of the stored lead, or None if the lead could not be stored
    """
    # Implementation details as shown in the TinyDB Storage Node section
    pass
```

### Enhanced Conversation Storage Logic

```python
def store_conversation(conversation_history, db_path=None):
    """Store conversation history in TinyDB.
    
    This function stores the complete conversation history in the TinyDB database for future reference.
    
    Args:
        conversation_history: List of message objects representing the conversation
        db_path: Path to TinyDB database
        
    Returns:
        The ID of the stored conversation
    """
    # Implementation details as shown in the Conversation Storage Node section
    pass
```

## Pipeline Integration

The pipeline is integrated into the FastAPI backend through the `chat_handler.py` module. The handler:

1. Receives user messages from the API
2. Passes them to the LangFlow pipeline
3. Receives responses from the pipeline
4. Returns the responses to the API

## Testing and Validation

The pipeline should be tested with various conversation scenarios to ensure it:

1. Follows the conversation flow outlined in the system prompt
2. Correctly retrieves guidance information from TinyDB
3. Accurately extracts lead information from conversations
4. Properly stores leads in TinyDB when appropriate
5. Maintains conversation context throughout the interaction

## Error Handling

The pipeline should include error handling for:

1. Invalid user inputs
2. LLM API errors
3. Error handling (TinyDB connection issues, LLM API errors)
4. Missing or invalid guidance data

## Security Considerations

1. **Credential Management**: Store API keys securely and never expose them in the frontend.
2. **Data Validation**: Validate all data before storing in TinyDB to prevent injection attacks.
3. **Input Sanitization**: Sanitize user inputs to prevent prompt injection.
4. **Access Control**: Implement appropriate access controls for the TinyDB collections.

## Conclusion

This LangFlow pipeline design provides a comprehensive framework for the pre-sales chatbot. By integrating the system prompt, guidance tools, and TinyDB storage, the pipeline enables natural conversations with potential clients while collecting valuable lead information.

The design emphasizes flexibility, allowing for easy updates to the system prompt, guidance data, and language model. It also incorporates robust error handling and security considerations to ensure reliable operation.

Regular testing and refinement of the pipeline will be essential to optimize the chatbot's performance and lead generation capabilities. 