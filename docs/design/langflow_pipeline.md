# LangFlow Pipeline Design

## Overview
This document outlines the design of the LangFlow pipeline for the pre-sales chatbot. The pipeline orchestrates the conversation flow, processes user messages, generates responses, extracts lead information, and triggers lead storage in Firebase. This design incorporates the conversation flow and data schema defined in their respective design documents.

## Pipeline Components

### 1. Input Node
- Receives the user's message and session context
- Passes the message to the conversation chain
- Includes user_id for tracking conversations

### 2. System Prompt Node
- Contains the system prompt that guides the chatbot's behavior
- Can be updated without modifying code
- Defines the conversation flow, tone, and lead collection strategy
- Includes instructions for handling standard and non-standard projects

### 3. Conversation Memory Node
- Maintains the conversation history
- Allows the chatbot to reference previous messages
- Provides context for the language model
- Stores conversation state for tracking progress

### 4. LiteLLM Node
- Connects to the language model provider (e.g., OpenAI, Anthropic)
- Processes the user message, system prompt, and conversation history
- Generates the chatbot's response
- Configured for Python 3.11 compatibility

### 5. Budget Guidance Tool Node
- Retrieves budget guidance from Firebase based on project type
- Formats the guidance data for presentation to the user
- Handles cases where project type is not found
- Returns structured budget information

### 6. Timeline Guidance Tool Node
- Retrieves timeline guidance from Firebase based on project type
- Formats the guidance data for presentation to the user
- Handles cases where project type is not found
- Returns structured timeline information including project phases

### 7. Project Type Detection Node
- Analyzes conversation to identify the project type
- Maps user descriptions to standard project categories
- Flags non-standard project types for special handling
- Updates conversation context with detected project type

### 8. Lead Extraction Node
- Analyzes the conversation to extract lead information
- Identifies when sufficient information has been collected
- Determines when the user has given consent for follow-up
- Structures data according to the Leads collection schema

### 9. Firebase Storage Node
- Receives lead information from the Lead Extraction Node
- Validates the data for completeness
- Stores the lead in Firebase Firestore
- Returns a success/failure message

### 10. Conversation Storage Node
- Stores the complete conversation history in Firebase
- Links conversation to lead if one was created
- Captures metadata like conversation duration and message count
- Enables future analysis and improvement

### 11. Output Node
- Formats the chatbot's response for the frontend
- Includes the response text, session ID, and lead storage status
- Provides context for the next user interaction

## Enhanced Pipeline Flow

```
┌─────────────┐     ┌───────────────┐     ┌─────────────────┐
│  Input Node │────►│ System Prompt │────►│ Conversation    │
└─────────────┘     │     Node      │     │  Memory Node    │
                    └───────────────┘     └────────┬────────┘
                                                   │
                                                   ▼
┌─────────────┐     ┌───────────────┐     ┌─────────────────┐
│ Output Node │◄────│ Project Type  │◄────│    LiteLLM      │
└──────┬──────┘     │ Detection Node│     │     Node        │
       │            └───────┬───────┘     └────────┬────────┘
       │                    │                      │
       │                    │                      │
       │                    ▼                      │
       │            ┌───────────────┐              │
       │            │ Budget/Timeline│◄─────────────┘
       │            │ Guidance Tools│
       │            └───────┬───────┘
       │                    │
       │                    ▼
       │            ┌───────────────┐
       │            │ Lead          │
       │            │ Extraction    │
       │            └───────┬───────┘
       │                    │
       │                    ▼
       │            ┌───────────────┐
       └───────────►│ Firebase      │
                    │ Storage Nodes │
                    └───────────────┘
```

## Node Configurations

### 1. Input Node
- **Type**: InputNode
- **Parameters**:
  - `message`: The user's message
  - `session_id`: Unique identifier for the conversation
  - `user_id`: Identifier for the user (for conversation tracking)

### 2. System Prompt Node
- **Type**: SystemPromptNode
- **Parameters**:
  - `prompt_text`: The system prompt text (see `system_prompt.md`)
  - `conversation_flow`: Reference to the conversation flow design

### 3. Conversation Memory Node
- **Type**: ConversationBufferMemory
- **Parameters**:
  - `memory_key`: "chat_history"
  - `return_messages`: true
  - `output_key`: "output"
  - `input_key`: "input"
  - `human_prefix`: "User"
  - `ai_prefix`: "Assistant"

### 4. LiteLLM Node
- **Type**: LiteLLMNode
- **Parameters**:
  - `model`: The language model to use (e.g., "gpt-4o-mini", "claude-3-sonnet")
  - `temperature`: 0.7 (adjust for more/less creative responses)
  - `max_tokens`: 800 (adjust based on expected response length)
  - `top_p`: 0.95
  - `frequency_penalty`: 0.0
  - `presence_penalty`: 0.0

### 5. Budget Guidance Tool Node
- **Type**: PythonFunctionNode
- **Parameters**:
  - `function`: get_budget_guidance
  - `project_type`: Project type detected from conversation
  - `format_output`: true

### 6. Timeline Guidance Tool Node
- **Type**: PythonFunctionNode
- **Parameters**:
  - `function`: get_timeline_guidance
  - `project_type`: Project type detected from conversation
  - `format_output`: true

### 7. Project Type Detection Node
- **Type**: PythonFunctionNode
- **Parameters**:
  - `function`: detect_project_type
  - `conversation_history`: The conversation history
  - `standard_project_types`: List of standard project types

### 8. Lead Extraction Node
- **Type**: PythonFunctionNode
- **Parameters**:
  - `function`: extract_lead_info
  - `conversation_history`: The conversation history
  - `required_fields`: List of required fields for a complete lead
  - `project_type`: Detected project type

### 9. Firebase Storage Node (Leads)
- **Type**: PythonFunctionNode
- **Parameters**:
  - `function`: store_lead
  - `lead_data`: Dictionary containing lead information
  - `credentials_path`: Path to Firebase credentials

### 10. Conversation Storage Node
- **Type**: PythonFunctionNode
- **Parameters**:
  - `function`: store_conversation
  - `conversation_history`: The complete conversation history
  - `user_id`: User identifier
  - `session_id`: Session identifier
  - `lead_id`: ID of the lead if one was created
  - `credentials_path`: Path to Firebase credentials

### 11. Output Node
- **Type**: OutputNode
- **Parameters**:
  - `response`: The chatbot's response text
  - `session_id`: The session ID
  - `lead_stored`: Boolean indicating whether a lead was stored
  - `detected_project_type`: The detected project type

## Implementation Details

### Project Type Detection Logic

```python
def detect_project_type(conversation_history, standard_project_types):
    """Detect the project type from conversation history.
    
    Args:
        conversation_history (list): List of conversation messages
        standard_project_types (list): List of standard project types
        
    Returns:
        dict: Detection results with project type and confidence
    """
    # Extract user messages
    user_messages = [msg["content"] for msg in conversation_history if msg["role"] == "user"]
    combined_text = " ".join(user_messages).lower()
    
    # Define project type keywords
    project_keywords = {
        "Basic website": ["basic website", "simple website", "informational website", "small website", "brochure site"],
        "E-commerce site": ["e-commerce", "online store", "shop", "selling online", "product catalog"],
        "Mobile app": ["mobile app", "ios app", "android app", "smartphone app", "tablet app"],
        "Custom software": ["custom software", "bespoke software", "enterprise software", "internal system"]
    }
    
    # Check for matches
    matches = {}
    for project_type, keywords in project_keywords.items():
        score = 0
        for keyword in keywords:
            if keyword in combined_text:
                score += 1
        if score > 0:
            matches[project_type] = score
    
    # Determine best match
    if matches:
        best_match = max(matches.items(), key=lambda x: x[1])
        is_standard = True
        confidence = best_match[1] / len(project_keywords[best_match[0]])
        project_type = best_match[0]
    else:
        # No standard project type detected
        is_standard = False
        confidence = 0.0
        project_type = "Non-standard project"
    
    return {
        "project_type": project_type,
        "is_standard_project": is_standard,
        "confidence": confidence,
        "requires_custom_assessment": not is_standard
    }
```

### Enhanced Budget Guidance Tool

```python
def get_budget_guidance(project_type=None):
    """Get budget guidance for a specific project type or all types.
    
    Args:
        project_type (str, optional): The type of project to get guidance for.
            If None, returns guidance for all project types.
            
    Returns:
        dict: Budget guidance information with formatted display text.
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
    
    # Format the guidance for display
    formatted_guidance = format_budget_guidance(guidance)
    
    return {
        "raw_guidance": guidance,
        "formatted_guidance": formatted_guidance,
        "project_type": project_type,
        "found": len(guidance) > 0
    }
```

### Enhanced Timeline Guidance Tool

```python
def get_timeline_guidance(project_type=None):
    """Get timeline guidance for a specific project type or all types.
    
    Args:
        project_type (str, optional): The type of project to get guidance for.
            If None, returns guidance for all project types.
            
    Returns:
        dict: Timeline guidance information with formatted display text and phases.
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
    
    # Format the guidance for display
    formatted_guidance = format_timeline_guidance(guidance)
    
    # Extract phases if available
    phases = []
    if guidance and len(guidance) > 0 and 'phases' in guidance[0]:
        phases = guidance[0]['phases']
    
    return {
        "raw_guidance": guidance,
        "formatted_guidance": formatted_guidance,
        "project_type": project_type,
        "phases": phases,
        "found": len(guidance) > 0
    }
```

### Enhanced Lead Extraction Logic

```python
def extract_lead_info(conversation_history, required_fields, project_type):
    """Extract lead information from conversation history.
    
    Args:
        conversation_history (list): List of conversation messages
        required_fields (list): List of required fields for a complete lead
        project_type (str): Detected project type
        
    Returns:
        dict: Extracted lead information and status
    """
    # Initialize lead data structure based on schema
    lead_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "client_name": None,
        "client_business": None,
        "contact_information": None,
        "project_description": None,
        "features": [],
        "timeline": None,
        "budget_range": None,
        "confirmed_follow_up": False,
        "is_standard_project": project_type != "Non-standard project",
        "requires_custom_assessment": project_type == "Non-standard project",
        "additional_notes": "",
        "project_type": project_type,
        "lead_source": "chatbot",
        "status": "new",
        "assigned_to": "",
        "last_contact": None
    }
    
    # Extract user messages
    user_messages = [msg["content"] for msg in conversation_history if msg["role"] == "user"]
    assistant_messages = [msg["content"] for msg in conversation_history if msg["role"] == "assistant"]
    combined_text = " ".join(user_messages)
    
    # Extract information using NER, regex patterns, and heuristics
    # This is a simplified example - in production, use more sophisticated NLP
    
    # Extract name (look for patterns like "my name is [name]" or "I'm [name]")
    name_patterns = [
        r"(?i)my name is\s+([A-Za-z\s]+)",
        r"(?i)i am\s+([A-Za-z\s]+)",
        r"(?i)i'm\s+([A-Za-z\s]+)",
        r"(?i)this is\s+([A-Za-z\s]+)"
    ]
    
    for pattern in name_patterns:
        matches = re.findall(pattern, combined_text)
        if matches:
            # Clean up the extracted name
            lead_data["client_name"] = matches[0].strip().split(" from ")[0]
            break
    
    # Extract email (simple pattern)
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    email_matches = re.findall(email_pattern, combined_text)
    if email_matches:
        lead_data["contact_information"] = email_matches[0]
    
    # Extract phone (simple pattern)
    phone_pattern = r"(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    phone_matches = re.findall(phone_pattern, combined_text)
    if phone_matches and not lead_data["contact_information"]:
        lead_data["contact_information"] = phone_matches[0]
    
    # Extract business name
    business_patterns = [
        r"(?i)my (company|business) is\s+([A-Za-z0-9\s]+)",
        r"(?i)for\s+([A-Za-z0-9\s]+)(?:\s+company|\s+business|\s+store|\s+shop)",
        r"(?i)work for\s+([A-Za-z0-9\s]+)"
    ]
    
    for pattern in business_patterns:
        matches = re.findall(pattern, combined_text)
        if matches:
            if isinstance(matches[0], tuple):
                lead_data["client_business"] = matches[0][1].strip()
            else:
                lead_data["client_business"] = matches[0].strip()
            break
    
    # Extract project description
    # This is simplified - in production, use more sophisticated NLP
    if project_type != "Non-standard project":
        lead_data["project_description"] = f"{project_type} for {lead_data['client_business'] or 'their business'}"
    else:
        # For non-standard projects, try to construct a description from the conversation
        project_desc_patterns = [
            r"(?i)need\s+([^.!?]+)",
            r"(?i)looking for\s+([^.!?]+)",
            r"(?i)want to build\s+([^.!?]+)",
            r"(?i)interested in\s+([^.!?]+)"
        ]
        
        for pattern in project_desc_patterns:
            matches = re.findall(pattern, combined_text)
            if matches:
                lead_data["project_description"] = matches[0].strip()
                break
    
    # Extract features
    feature_indicators = ["features", "functionality", "include", "support", "capabilities"]
    for indicator in feature_indicators:
        pattern = f"(?i){indicator}[^.!?]*?([^.!?]+)"
        matches = re.findall(pattern, combined_text)
        for match in matches:
            # Split by commas or "and"
            features = re.split(r",|\sand\s", match)
            lead_data["features"].extend([f.strip() for f in features if f.strip()])
    
    # Extract timeline
    timeline_patterns = [
        r"(?i)timeline[^.!?]*?([^.!?]+)",
        r"(?i)complete in\s+([^.!?]+)",
        r"(?i)finished by\s+([^.!?]+)",
        r"(?i)ready in\s+([^.!?]+)",
        r"(?i)launch in\s+([^.!?]+)"
    ]
    
    for pattern in timeline_patterns:
        matches = re.findall(pattern, combined_text)
        if matches:
            lead_data["timeline"] = matches[0].strip()
            break
    
    # Extract budget
    budget_patterns = [
        r"(?i)budget[^.!?]*?([^.!?]+)",
        r"(?i)spend[^.!?]*?([^.!?]+)",
        r"(?i)cost[^.!?]*?([^.!?]+)",
        r"(?i)\$\s*(\d[\d,.]*\s*(?:thousand|k|million|m)?)",
        r"(?i)(\d[\d,.]*\s*(?:thousand|k|million|m)?\s*dollars)"
    ]
    
    for pattern in budget_patterns:
        matches = re.findall(pattern, combined_text)
        if matches:
            lead_data["budget_range"] = matches[0].strip()
            break
    
    # Check for follow-up consent
    consent_indicators = [
        r"(?i)yes,?\s+you can (?:contact|email|call|reach)",
        r"(?i)that'?s fine",
        r"(?i)(?:contact|email|call|reach) me",
        r"(?i)(?:happy|okay|fine) to (?:be contacted|receive)",
        r"(?i)(?:sure|yes|yeah|ok|okay),?\s+(?:that'?s|that is)?\s*(?:fine|good|okay)"
    ]
    
    # Look for consent in the last few user messages (more relevant)
    recent_messages = user_messages[-3:] if len(user_messages) > 3 else user_messages
    recent_text = " ".join(recent_messages)
    
    for pattern in consent_indicators:
        if re.search(pattern, recent_text):
            lead_data["confirmed_follow_up"] = True
            break
    
    # Check if all required fields are present
    is_complete = all(lead_data.get(field) for field in required_fields)
    
    # Check if follow-up consent was given
    has_consent = lead_data.get("confirmed_follow_up", False)
    
    return {
        "lead_data": lead_data,
        "is_complete": is_complete,
        "has_consent": has_consent,
        "missing_fields": [field for field in required_fields if not lead_data.get(field)]
    }
```

### Enhanced Firebase Storage Logic

```python
def store_lead(lead_data, credentials_path):
    """Store lead information in Firebase.
    
    Args:
        lead_data (dict): Dictionary containing lead information
        credentials_path (str): Path to Firebase credentials
        
    Returns:
        dict: Result of the storage operation
    """
    # Initialize Firebase
    from firebase_handler import FirebaseHandler
    
    # Create Firebase handler
    firebase = FirebaseHandler(credentials_path)
    
    # Validate required fields
    required_fields = ["client_name", "contact_information", "project_description", "confirmed_follow_up"]
    missing_fields = [field for field in required_fields if not lead_data.get(field)]
    
    if missing_fields:
        return {
            "success": False,
            "error": f"Missing required fields: {', '.join(missing_fields)}",
            "message": "Failed to store lead due to missing information"
        }
    
    # Ensure confirmed_follow_up is True
    if not lead_data.get("confirmed_follow_up", False):
        return {
            "success": False,
            "error": "User has not consented to follow-up",
            "message": "Cannot store lead without explicit consent"
        }
    
    # Add timestamp if not present
    if "timestamp" not in lead_data:
        lead_data["timestamp"] = datetime.datetime.now().isoformat()
    
    # Add default status if not present
    if "status" not in lead_data:
        lead_data["status"] = "new"
    
    # Store lead
    try:
        lead_id = firebase.add_document("leads", lead_data)
        return {
            "success": True,
            "lead_id": lead_id,
            "message": "Lead stored successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to store lead due to a database error"
        }
```

### Conversation Storage Logic

```python
def store_conversation(conversation_history, user_id, session_id, lead_id, credentials_path):
    """Store conversation history in Firebase.
    
    Args:
        conversation_history (list): List of conversation messages
        user_id (str): User identifier
        session_id (str): Session identifier
        lead_id (str): ID of the lead if one was created
        credentials_path (str): Path to Firebase credentials
        
    Returns:
        dict: Result of the storage operation
    """
    # Initialize Firebase
    from firebase_handler import FirebaseHandler
    
    # Create Firebase handler
    firebase = FirebaseHandler(credentials_path)
    
    # Calculate conversation metrics
    created_at = conversation_history[0]["timestamp"] if "timestamp" in conversation_history[0] else datetime.datetime.now().isoformat()
    updated_at = datetime.datetime.now().isoformat()
    message_count = len(conversation_history)
    
    # Try to detect project type from conversation
    project_types = ["Basic website", "E-commerce site", "Mobile app", "Custom software"]
    detected_project_type = None
    
    for msg in conversation_history:
        if msg["role"] == "assistant" and any(pt in msg["content"] for pt in project_types):
            for pt in project_types:
                if pt in msg["content"]:
                    detected_project_type = pt
                    break
            if detected_project_type:
                break
    
    # Prepare conversation data
    conversation_data = {
        "user_id": user_id,
        "session_id": session_id,
        "messages": conversation_history,
        "created_at": created_at,
        "updated_at": updated_at,
        "lead_id": lead_id or "",
        "conversation_summary": "",  # Could be generated with an additional LLM call
        "detected_project_type": detected_project_type or "Unknown",
        "conversation_duration": 0,  # Would need start/end timestamps to calculate
        "message_count": message_count
    }
    
    # Store conversation
    try:
        conversation_id = firebase.add_document("conversations", conversation_data)
        return {
            "success": True,
            "conversation_id": conversation_id,
            "message": "Conversation stored successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to store conversation due to a database error"
        }
```

## Tool Registration in LangFlow

To make the guidance tools available to the LLM, they need to be registered in the LangFlow pipeline:

```python
def register_tools(flow):
    """Register custom tools with the LangFlow pipeline."""
    # Register budget and timeline guidance tools
    flow.add_tool(get_budget_guidance)
    flow.add_tool(get_timeline_guidance)
    
    # Register project type detection
    flow.add_tool(detect_project_type)
    
    # Register lead extraction and storage tools
    flow.add_tool(extract_lead_info)
    flow.add_tool(store_lead)
    flow.add_tool(store_conversation)
    
    return flow
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
3. Edit the prompt text based on the conversation flow design
4. Save the pipeline
5. Export the updated pipeline

### Changing the Language Model
1. Open the pipeline in LangFlow
2. Find the LiteLLM Node
3. Update the model parameter (e.g., to "gpt-4o-mini" or "claude-3-sonnet")
4. Adjust other parameters as needed (temperature, max_tokens)
5. Save the pipeline
6. Export the updated pipeline

### Updating Guidance Tools
1. Modify the guidance tool functions in `guidance_tools.py`
2. Update the Firebase collections with new guidance data
3. Test the tools in isolation
4. Update the pipeline to use the new tool versions

## Testing the Pipeline

### Manual Testing
1. Import the pipeline into LangFlow
2. Use the LangFlow UI to test the pipeline with example messages
3. Verify that the chatbot responds appropriately
4. Check that project types are correctly detected
5. Verify that guidance tools provide accurate information
6. Confirm that lead information is extracted correctly
7. Ensure that leads are stored in Firebase when appropriate

### Automated Testing
Create test cases for:
1. Different conversation scenarios (standard and non-standard projects)
2. Edge cases (missing information, unclear responses)
3. Error handling (Firebase connection issues, LLM API errors)
4. Tool functionality (guidance retrieval, lead extraction)

## Performance Considerations

1. **Memory Usage**: The conversation memory can grow large with lengthy conversations. Consider implementing a windowing mechanism to limit the context size.

2. **Token Optimization**: Be mindful of token usage in the system prompt and conversation history. Use concise language and consider summarizing older parts of the conversation.

3. **Error Recovery**: Implement robust error handling for all tool calls, especially Firebase operations.

4. **Caching**: Consider caching guidance data to reduce database calls.

## Security Considerations

1. **Credential Management**: Store Firebase credentials securely and never expose them in the frontend.

2. **Data Validation**: Validate all data before storing in Firebase to prevent injection attacks.

3. **User Consent**: Always obtain explicit consent before storing personal information.

4. **Access Control**: Implement appropriate access controls for the Firebase collections.

## Conclusion

This LangFlow pipeline design provides a comprehensive framework for implementing the pre-sales chatbot. By integrating the conversation flow design and data schema, the pipeline ensures a natural, effective conversation that collects lead information while providing valuable guidance to potential clients.

The design emphasizes flexibility, allowing for easy updates to the system prompt, guidance data, and language model. It also incorporates robust error handling and security considerations to ensure reliable operation.

Regular testing and refinement of the pipeline will be essential to optimize the chatbot's performance and lead generation capabilities. 