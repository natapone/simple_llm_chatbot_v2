"""
LangFlow Pipeline Configuration for Pre-Sales Chatbot

This module defines the LangFlow pipeline configuration for the pre-sales chatbot.
It includes the system prompt, conversation memory, and integration with guidance tools.
"""

import os
import re
import time
from typing import List, Dict, Any, Optional
import datetime
import json
import logging
from dotenv import load_dotenv
from litellm import completion

# Load environment variables
load_dotenv()

# Import the guidance tools
from app.guidance_tools import get_budget_guidance, get_timeline_guidance
from app.database_handler import DatabaseHandler

# System prompt for the chatbot
SYSTEM_PROMPT = """
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

# Standard project types for detection
STANDARD_PROJECT_TYPES = ["e-commerce", "corporate", "blog", "mobile app", "web application", "api", "dashboard"]

def detect_project_type(conversation_history: List[Dict[str, Any]]) -> Optional[str]:
    """Detect the project type from the conversation history.
    
    Args:
        conversation_history: The conversation history
        
    Returns:
        The detected project type or None if no project type is detected
    """
    # Convert conversation history to a single string for analysis
    conversation_text = " ".join([msg["content"] for msg in conversation_history])
    conversation_text = conversation_text.lower()
    
    # Check for standard project types
    for project_type in STANDARD_PROJECT_TYPES:
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

def extract_entity_with_llm(conversation_text: str, entity_type: str, max_retries: int = 2) -> Optional[str]:
    """Extract an entity from conversation text using LiteLLM.
    
    Args:
        conversation_text: The conversation text to extract from
        entity_type: The type of entity to extract (name, email, business, etc.)
        max_retries: Maximum number of retry attempts if the API call fails
        
    Returns:
        The extracted entity or None if not found
    """
    # Force reload environment variables
    load_dotenv(override=True)
    
    # Configure LiteLLM with environment variables
    api_key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")  # Using a simpler model for entity extraction
    
    # Set the API key directly in the environment
    os.environ["OPENAI_API_KEY"] = api_key
    
    # Log the API key (masked)
    masked_key = api_key[:5] + "..." + api_key[-4:] if api_key and len(api_key) > 10 else "None"
    print(f"Using API key: {masked_key}")
    
    # Check if we have a cached response for this conversation and entity type
    # This is a simple in-memory cache - could be replaced with a more robust solution
    cache_key = f"{hash(conversation_text)}:{entity_type}"
    if hasattr(extract_entity_with_llm, "cache") and cache_key in extract_entity_with_llm.cache:
        return extract_entity_with_llm.cache[cache_key]
    
    # Create a more detailed prompt for entity extraction
    prompt = f"""
    You are an AI assistant specialized in extracting specific information from conversations.
    
    Please extract the {entity_type} from the following conversation. Return ONLY the extracted information, nothing else.
    If you cannot find the information, respond with "Not found".
    
    Guidelines:
    - For client names, extract the full name
    - For business names, extract the complete business name
    - For project descriptions, extract a concise description
    - For features, extract a comma-separated list
    - For timelines, extract the specific timeframe
    - For budget ranges, extract the specific amount or range
    - For follow-up consent, extract "yes" or "no"
    
    CONVERSATION:
    {conversation_text}
    
    {entity_type.upper()}:
    """
    
    # Initialize retry counter
    retry_count = 0
    
    while retry_count <= max_retries:
        try:
            # Call LiteLLM for entity extraction with temperature 0 for more consistent results
            response = completion(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=50,
                api_key=api_key  # Explicitly pass the API key
            )
            
            # Extract the response
            extracted_text = response.choices[0].message.content.strip()
            
            # Return None if no entity was found
            if extracted_text.lower() in ["not found", "none", "n/a", "unknown"]:
                return None
                
            # Cache the result
            if not hasattr(extract_entity_with_llm, "cache"):
                extract_entity_with_llm.cache = {}
            extract_entity_with_llm.cache[cache_key] = extracted_text
            
            return extracted_text
            
        except Exception as e:
            retry_count += 1
            print(f"Error extracting entity with LiteLLM (attempt {retry_count}/{max_retries + 1}): {str(e)}")
            
            # Wait before retrying (exponential backoff)
            if retry_count <= max_retries:
                time.sleep(2 ** retry_count)
    
    # If all retries failed, return None
    return None

def extract_with_regex(conversation_text: str, entity_type: str) -> Optional[str]:
    """Extract an entity from conversation text using regex patterns as fallback.
    
    Args:
        conversation_text: The conversation text to extract from
        entity_type: The type of entity to extract (name, email, business, etc.)
        
    Returns:
        The extracted entity or None if not found
    """
    if entity_type == "client name":
        # Patterns to extract client name
        name_patterns = [
            r"my name is ([A-Za-z\s]+?)(?:\s+and|\s*,|\s*\.|$)",
            r"I'm ([A-Za-z\s]+?)(?:\s+and|\s*,|\s*\.|$)",
            r"I am ([A-Za-z\s]+?)(?:\s+and|\s*,|\s*\.|$)",
            r"([A-Za-z\s]+?) here"
        ]
        
        for pattern in name_patterns:
            matches = re.search(pattern, conversation_text)
            if matches:
                return matches.group(1).strip()
    
    elif entity_type == "business name":
        # Patterns to extract business name
        business_patterns = [
            r"(?:my|our) (?:company|business) (?:is|name is) ([A-Za-z0-9\s&]+)",
            r"(?:I work for|I represent|I own) ([A-Za-z0-9\s&]+)",
            r"([A-Za-z0-9\s&]+) (?:company|business)"
        ]
        
        for pattern in business_patterns:
            matches = re.search(pattern, conversation_text)
            if matches:
                return matches.group(1).strip()
    
    elif entity_type == "project description":
        # Patterns to extract project description
        description_patterns = [
            r"(?:looking to|want to|need to|interested in) ([^.]+)",
            r"(?:build|create|develop) ([^.]+)",
            r"(?:project|website|application|app) (?:for|that) ([^.]+)"
        ]
        
        for pattern in description_patterns:
            matches = re.search(pattern, conversation_text)
            if matches:
                return matches.group(1).strip()
    
    elif entity_type == "project timeline":
        # Patterns to extract timeline
        timeline_patterns = [
            r"(?:timeline|timeframe|deadline) (?:is|of) ([^.]+)",
            r"(?:complete|finish|deliver) (?:in|within) ([^.]+)",
            r"(?:need|want) it (?:in|within|by) ([^.]+)"
        ]
        
        for pattern in timeline_patterns:
            matches = re.search(pattern, conversation_text)
            if matches:
                return matches.group(1).strip()
    
    elif entity_type == "budget range":
        # Patterns to extract budget
        budget_patterns = [
            r"(?:budget|price|cost) (?:is|of) ([^.]+)",
            r"(?:willing to|can|could) (?:pay|spend) ([^.]+)",
            r"(?:around|about|approximately) \$([\d,]+(?:\s*-\s*\$?[\d,]+)?)"
        ]
        
        for pattern in budget_patterns:
            matches = re.search(pattern, conversation_text)
            if matches:
                return matches.group(1).strip()
    
    elif entity_type == "project features":
        # Patterns to extract features
        features_patterns = [
            r"(?:features|functionality) (?:like|such as|including) ([^.]+)",
            r"(?:need|want|require) (?:to have|to include) ([^.]+)",
            r"(?:should have|must have|would like) ([^.]+)"
        ]
        
        for pattern in features_patterns:
            matches = re.search(pattern, conversation_text)
            if matches:
                features_text = matches.group(1).strip()
                return features_text
    
    elif entity_type == "follow-up consent (yes/no)":
        # Patterns to check for follow-up consent
        consent_patterns = [
            r"(?:yes|sure|okay|fine|alright)[,\.]? (?:you can|please) (?:contact|email|call|follow up)",
            r"(?:feel free to|please) (?:contact|email|call|follow up)",
            r"(?:happy to|willing to) (?:discuss|talk|chat) (?:more|further|again)"
        ]
        
        for pattern in consent_patterns:
            if re.search(pattern, conversation_text, re.IGNORECASE):
                return "yes"
        
        return "no"
    
    return None

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
    
    # Extract client name using LiteLLM with regex fallback
    lead_data["client_name"] = extract_entity_with_llm(conversation_text, "client name")
    if lead_data["client_name"] is None:
        lead_data["client_name"] = extract_with_regex(conversation_text, "client name")
    
    # Extract client business using LiteLLM with regex fallback
    lead_data["client_business"] = extract_entity_with_llm(conversation_text, "business name")
    if lead_data["client_business"] is None:
        lead_data["client_business"] = extract_with_regex(conversation_text, "business name")
    
    # Extract contact information (email) using regex
    # Email is better extracted with regex for accuracy
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_matches = re.findall(email_pattern, conversation_text)
    if email_matches:
        lead_data["contact_information"] = email_matches[0]
    
    # Extract project description using LiteLLM with regex fallback
    lead_data["project_description"] = extract_entity_with_llm(conversation_text, "project description")
    if lead_data["project_description"] is None:
        lead_data["project_description"] = extract_with_regex(conversation_text, "project description")
    
    # Extract features using LiteLLM with regex fallback
    features_text = extract_entity_with_llm(conversation_text, "project features")
    if features_text is None:
        features_text = extract_with_regex(conversation_text, "project features")
    
    if features_text:
        # Split features by commas if multiple features are returned
        features = [f.strip() for f in features_text.split(",")]
        lead_data["features"] = features
    
    # Extract timeline using LiteLLM with regex fallback
    lead_data["timeline"] = extract_entity_with_llm(conversation_text, "project timeline")
    if lead_data["timeline"] is None:
        lead_data["timeline"] = extract_with_regex(conversation_text, "project timeline")
    
    # Extract budget range using LiteLLM with regex fallback
    lead_data["budget_range"] = extract_entity_with_llm(conversation_text, "budget range")
    if lead_data["budget_range"] is None:
        lead_data["budget_range"] = extract_with_regex(conversation_text, "budget range")
    
    # Check for follow-up consent using LiteLLM with regex fallback
    consent_text = extract_entity_with_llm(conversation_text, "follow-up consent (yes/no)")
    if consent_text is None:
        consent_text = extract_with_regex(conversation_text, "follow-up consent (yes/no)")
    
    if consent_text and consent_text.lower() in ["yes", "true", "confirmed"]:
        lead_data["confirmed_follow_up"] = True
    
    return lead_data

def store_lead(lead_data: Dict[str, Any], db_path: str = None) -> Optional[int]:
    """Store lead information in TinyDB.
    
    Args:
        lead_data: Dictionary containing lead information
        db_path: Path to TinyDB database
        
    Returns:
        The ID of the stored lead, or None if the lead could not be stored
    """
    # Check if all required fields are present
    required_fields = ["client_name", "contact_information", "confirmed_follow_up"]
    for field in required_fields:
        if not lead_data.get(field):
            return None
    
    # Only store if follow-up is confirmed
    if not lead_data["confirmed_follow_up"]:
        return None
    
    # Get database path from environment if not provided
    if not db_path:
        db_path = os.getenv("TINYDB_PATH", "./data/chatbot_db.json")
    
    # Initialize database handler
    db_handler = DatabaseHandler(db_path)
    
    # Store lead in database
    try:
        lead_id = db_handler.add_document("leads", lead_data)
        return lead_id
    except Exception as e:
        print(f"Error storing lead: {str(e)}")
        return None

def store_conversation(conversation_history: List[Dict[str, Any]], session_id: str, user_id: str, db_path: str = None) -> Optional[int]:
    """Store conversation history in TinyDB.
    
    Args:
        conversation_history: List of message objects representing the conversation
        session_id: The session ID for the conversation
        user_id: The user ID for the conversation
        db_path: Path to TinyDB database
        
    Returns:
        The ID of the stored conversation, or None if the conversation could not be stored
    """
    # Get database path from environment if not provided
    if not db_path:
        db_path = os.getenv("TINYDB_PATH", "./data/chatbot_db.json")
    
    # Initialize database handler
    db_handler = DatabaseHandler(db_path)
    
    # Prepare conversation data
    conversation_data = {
        "user_id": user_id,
        "session_id": session_id,
        "messages": conversation_history,
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }
    
    # Store conversation in database
    try:
        conversation_id = db_handler.add_document("conversations", conversation_data)
        return conversation_id
    except Exception as e:
        print(f"Error storing conversation: {str(e)}")
        return None

def create_langflow_pipeline():
    """Create the LangFlow pipeline configuration.
    
    Returns:
        A dictionary containing the LangFlow pipeline configuration
    """
    # This is a simplified representation of the LangFlow pipeline
    # In a real implementation, this would be a JSON configuration for LangFlow
    pipeline = {
        "nodes": [
            {
                "id": "system_prompt",
                "type": "SystemMessagePromptTemplate",
                "data": {
                    "prompt": SYSTEM_PROMPT
                }
            },
            {
                "id": "human_message",
                "type": "HumanMessagePromptTemplate",
                "data": {
                    "prompt": "{input}"
                }
            },
            {
                "id": "chat_history",
                "type": "ConversationBufferMemory",
                "data": {
                    "memory_key": "chat_history",
                    "return_messages": True,
                    "output_key": "output",
                    "input_key": "input",
                    "human_prefix": "User",
                    "ai_prefix": "Assistant"
                }
            },
            {
                "id": "litellm",
                "type": "LiteLLMNode",
                "data": {
                    "model": os.getenv("LLM_MODEL", "gpt-4"),
                    "temperature": 0.7,
                    "max_tokens": 800
                }
            },
            {
                "id": "project_type_detection",
                "type": "PythonFunctionNode",
                "data": {
                    "function": "detect_project_type",
                    "conversation_history": "{chat_history}"
                }
            },
            {
                "id": "budget_guidance",
                "type": "PythonFunctionNode",
                "data": {
                    "function": "get_budget_guidance",
                    "project_type": "{project_type}"
                }
            },
            {
                "id": "timeline_guidance",
                "type": "PythonFunctionNode",
                "data": {
                    "function": "get_timeline_guidance",
                    "project_type": "{project_type}"
                }
            },
            {
                "id": "lead_extraction",
                "type": "PythonFunctionNode",
                "data": {
                    "function": "extract_lead_information",
                    "conversation_history": "{chat_history}"
                }
            },
            {
                "id": "tinydb_storage",
                "type": "PythonFunctionNode",
                "data": {
                    "function": "store_lead",
                    "lead_data": "{lead_data}",
                    "db_path": os.getenv("TINYDB_PATH", "./data/chatbot_db.json")
                }
            },
            {
                "id": "conversation_storage",
                "type": "PythonFunctionNode",
                "data": {
                    "function": "store_conversation",
                    "conversation_history": "{chat_history}",
                    "session_id": "{session_id}",
                    "user_id": "{user_id}",
                    "db_path": os.getenv("TINYDB_PATH", "./data/chatbot_db.json")
                }
            }
        ],
        "edges": [
            {"source": "system_prompt", "target": "litellm"},
            {"source": "human_message", "target": "litellm"},
            {"source": "chat_history", "target": "litellm"},
            {"source": "chat_history", "target": "project_type_detection"},
            {"source": "project_type_detection", "target": "budget_guidance"},
            {"source": "project_type_detection", "target": "timeline_guidance"},
            {"source": "chat_history", "target": "lead_extraction"},
            {"source": "lead_extraction", "target": "tinydb_storage"},
            {"source": "chat_history", "target": "conversation_storage"}
        ]
    }
    
    return pipeline

def save_pipeline_config(pipeline, file_path="app/langflow/pipeline.json"):
    """Save the pipeline configuration to a JSON file.
    
    Args:
        pipeline: The pipeline configuration
        file_path: The path to save the configuration to
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, "w") as f:
            json.dump(pipeline, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving pipeline configuration: {str(e)}")
        return False

# Generate and save the pipeline configuration when this module is imported
pipeline_config = create_langflow_pipeline()
save_pipeline_config(pipeline_config) 