# LangFlow Pipeline Design

## Overview
This document outlines the design of the LangFlow pipeline for the pre-sales chatbot. The pipeline orchestrates the conversation flow, processes user messages, generates responses, extracts lead information, and triggers lead storage in Firebase.

## Pipeline Components

### 1. Input Node
- Receives the user's message and session context
- Passes the message to the conversation chain

### 2. System Prompt Node
- Contains the system prompt that guides the chatbot's behavior
- Can be updated without modifying code
- Defines the conversation flow, tone, and lead collection strategy

### 3. Conversation Memory Node
- Maintains the conversation history
- Allows the chatbot to reference previous messages
- Provides context for the language model

### 4. LiteLLM Node
- Connects to the language model provider (e.g., OpenAI, Anthropic)
- Processes the user message, system prompt, and conversation history
- Generates the chatbot's response

### 5. Lead Extraction Node
- Analyzes the conversation to extract lead information
- Identifies when sufficient information has been collected
- Determines when the user has given consent for follow-up

### 6. Firebase Storage Node
- Receives lead information from the Lead Extraction Node
- Validates the data for completeness
- Stores the lead in Firebase Firestore
- Returns a success/failure message

### 7. Output Node
- Formats the chatbot's response for the frontend
- Includes the response text, session ID, and lead storage status

## Pipeline Flow

```
┌─────────────┐     ┌───────────────┐     ┌─────────────────┐
│  Input Node │────►│ System Prompt │────►│ Conversation    │
└─────────────┘     │     Node      │     │  Memory Node    │
                    └───────────────┘     └────────┬────────┘
                                                   │
                                                   ▼
┌─────────────┐     ┌───────────────┐     ┌─────────────────┐
│ Output Node │◄────│ Lead          │◄────│    LiteLLM      │
└─────────────┘     │ Extraction    │     │     Node        │
      ▲             │     Node      │     └─────────────────┘
      │             └───────┬───────┘
      │                     │
      │                     ▼
      │             ┌───────────────┐
      └─────────────│   Firebase    │
                    │ Storage Node  │
                    └───────────────┘
```

## Node Configurations

### 1. Input Node
- **Type**: InputNode
- **Parameters**:
  - `message`: The user's message
  - `session_id`: Unique identifier for the conversation

### 2. System Prompt Node
- **Type**: SystemPromptNode
- **Parameters**:
  - `prompt_text`: The system prompt text (see `system_prompt.md`)

### 3. Conversation Memory Node
- **Type**: ConversationBufferMemory
- **Parameters**:
  - `memory_key`: "chat_history"
  - `return_messages`: true

### 4. LiteLLM Node
- **Type**: LiteLLMNode
- **Parameters**:
  - `model`: The language model to use (e.g., "gpt-3.5-turbo", "claude-2")
  - `temperature`: 0.7 (adjust for more/less creative responses)
  - `max_tokens`: 500 (adjust based on expected response length)

### 5. Lead Extraction Node
- **Type**: CustomNode or PythonFunctionNode
- **Parameters**:
  - `conversation_history`: The conversation history
  - `required_fields`: List of required fields for a complete lead

### 6. Firebase Storage Node
- **Type**: CustomNode or PythonFunctionNode
- **Parameters**:
  - `lead_data`: Dictionary containing lead information
  - `credentials_path`: Path to Firebase credentials

### 7. Output Node
- **Type**: OutputNode
- **Parameters**:
  - `response`: The chatbot's response text
  - `session_id`: The session ID
  - `lead_stored`: Boolean indicating whether a lead was stored

## Lead Extraction Logic

The Lead Extraction Node will use the following logic to extract lead information:

```python
def extract_lead_info(conversation_history):
    """Extract lead information from conversation history."""
    lead_data = {
        "client_name": None,
        "client_business": None,
        "contact_information": None,
        "project_description": None,
        "features": [],
        "timeline": None,
        "budget_range": None,
        "confirmed_follow_up": False
    }
    
    # Analyze conversation to extract lead information
    # This can be done using regex patterns, NER, or custom logic
    
    # Check if all required fields are present
    required_fields = ["client_name", "contact_information", "project_description"]
    is_complete = all(lead_data.get(field) for field in required_fields)
    
    # Check if follow-up consent was given
    has_consent = lead_data.get("confirmed_follow_up", False)
    
    return {
        "lead_data": lead_data,
        "is_complete": is_complete,
        "has_consent": has_consent
    }
```

## Firebase Storage Logic

The Firebase Storage Node will use the following logic to store lead information:

```python
def store_lead(lead_data, credentials_path):
    """Store lead information in Firebase."""
    # Initialize Firebase
    from firebase_handler import FirebaseHandler
    
    # Create Firebase handler
    firebase = FirebaseHandler(credentials_path)
    
    # Store lead
    try:
        lead_id = firebase.store_lead(lead_data)
        return {
            "success": True,
            "lead_id": lead_id,
            "message": "Lead stored successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to store lead"
        }
```

## Exporting and Importing the Pipeline

### Exporting
1. In LangFlow, click on "Export" in the top-right corner
2. Select "Export as JSON"
3. Save the JSON file to the `langflow` directory

### Importing
1. In LangFlow, click on "Import" in the top-right corner
2. Select "Import from JSON"
3. Choose the JSON file from the `langflow` directory

## Customizing the Pipeline

### Updating the System Prompt
1. Open the pipeline in LangFlow
2. Find the System Prompt Node
3. Edit the prompt text
4. Save the pipeline
5. Export the updated pipeline

### Changing the Language Model
1. Open the pipeline in LangFlow
2. Find the LiteLLM Node
3. Update the model parameter
4. Adjust other parameters as needed (temperature, max_tokens)
5. Save the pipeline
6. Export the updated pipeline

## Testing the Pipeline

### Manual Testing
1. Import the pipeline into LangFlow
2. Use the LangFlow UI to test the pipeline with example messages
3. Verify that the chatbot responds appropriately
4. Check that lead information is extracted correctly
5. Confirm that leads are stored in Firebase when appropriate

### Automated Testing
Create test cases for:
1. Different conversation scenarios
2. Edge cases (missing information, unclear responses)
3. Error handling (Firebase connection issues, LLM API errors) 