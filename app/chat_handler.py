"""
Chat Handler Module

This module handles the processing of chat messages, including:
- Generating session IDs
- Storing conversation history
- Interacting with the LLM via LiteLLM
- Managing conversation context

Optimized for Python 3.11 with enhanced typing features.
"""

import os
import uuid
import logging
import json
from typing import Dict, List, Any, Optional, Tuple, TypedDict, Literal, Protocol, Union
from datetime import datetime

import pytz
import litellm
from firebase_handler import FirebaseHandler

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure LiteLLM
litellm.api_key = os.getenv("OPENAI_API_KEY")
litellm.set_verbose = True

class MessageRole(Protocol):
    """Protocol for message role types."""
    role: Literal["system", "user", "assistant"]
    content: str

class SystemMessage(TypedDict):
    """Type definition for system messages."""
    role: Literal["system"]
    content: str

class UserMessage(TypedDict):
    """Type definition for user messages."""
    role: Literal["user"]
    content: str

class AssistantMessage(TypedDict):
    """Type definition for assistant messages."""
    role: Literal["assistant"]
    content: str

Message = Union[SystemMessage, UserMessage, AssistantMessage]

class ConversationHistory(TypedDict):
    """Type definition for conversation history data."""
    user_id: str
    session_id: str
    messages: List[Message]
    created_at: str
    updated_at: str

def generate_session_id() -> str:
    """Generate a unique session ID.
    
    Returns:
        A unique session ID string.
    """
    return str(uuid.uuid4())

def get_system_prompt() -> str:
    """Get the system prompt for the chatbot.
    
    Returns:
        The system prompt string.
    """
    # Read from system_prompt.md file
    try:
        with open("system_prompt.md", "r") as f:
            system_prompt = f.read()
        return system_prompt
    except FileNotFoundError:
        logger.warning("system_prompt.md not found, using default prompt")
        return """
        You are a pre-sales chatbot for a software development company.
        Your role is to help potential clients understand our services and pricing.
        Be helpful, informative, and professional.
        """

def get_conversation_history(
    user_id: str, 
    session_id: str, 
    firebase_handler: FirebaseHandler
) -> List[Message]:
    """Get the conversation history for a user session.
    
    Args:
        user_id: The user's ID.
        session_id: The session ID.
        firebase_handler: The Firebase handler instance.
        
    Returns:
        A list of message dictionaries representing the conversation history.
    """
    logger.info(f"Getting conversation history for user {user_id}, session {session_id}")
    
    # Get conversation from Firebase
    conversation_data = firebase_handler.query_collection(
        "conversations",
        "session_id",
        "==",
        session_id
    )
    
    if conversation_data and len(conversation_data) > 0:
        # Return the messages from the conversation
        return conversation_data[0].get("messages", [])
    else:
        # No existing conversation, return empty list
        return []

def save_conversation_history(
    user_id: str, 
    session_id: str, 
    messages: List[Message], 
    firebase_handler: FirebaseHandler
) -> bool:
    """Save the conversation history to Firebase.
    
    Args:
        user_id: The user's ID.
        session_id: The session ID.
        messages: The list of message dictionaries.
        firebase_handler: The Firebase handler instance.
        
    Returns:
        True if the save was successful, False otherwise.
    """
    logger.info(f"Saving conversation history for user {user_id}, session {session_id}")
    
    # Get current timestamp
    timestamp = datetime.now(pytz.UTC).isoformat()
    
    # Check if conversation already exists
    conversation_data = firebase_handler.query_collection(
        "conversations",
        "session_id",
        "==",
        session_id
    )
    
    if conversation_data and len(conversation_data) > 0:
        # Update existing conversation
        conversation_id = conversation_data[0].get("id")
        return firebase_handler.update_document(
            "conversations",
            conversation_id,
            {
                "messages": messages,
                "updated_at": timestamp
            }
        )
    else:
        # Create new conversation
        conversation: ConversationHistory = {
            "user_id": user_id,
            "session_id": session_id,
            "messages": messages,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        document_id = firebase_handler.add_document("conversations", conversation)
        return document_id is not None

def process_chat_message(
    user_id: str, 
    message: str, 
    session_id: Optional[str], 
    firebase_handler: FirebaseHandler
) -> Tuple[str, str]:
    """Process a chat message and generate a response.
    
    Args:
        user_id: The user's ID.
        message: The message from the user.
        session_id: The session ID, or None if this is a new session.
        firebase_handler: The Firebase handler instance.
        
    Returns:
        A tuple containing (response_text, session_id).
    """
    logger.info(f"Processing message from user {user_id}")
    
    # Generate session ID if not provided
    if not session_id:
        session_id = generate_session_id()
        logger.info(f"Generated new session ID: {session_id}")
    
    # Get conversation history
    conversation_history = get_conversation_history(user_id, session_id, firebase_handler)
    
    # If this is a new conversation, add the system prompt
    if not conversation_history:
        system_message: SystemMessage = {
            "role": "system",
            "content": get_system_prompt()
        }
        conversation_history.append(system_message)
    
    # Add the user message to the history
    user_message: UserMessage = {
        "role": "user",
        "content": message
    }
    conversation_history.append(user_message)
    
    # Generate response using LiteLLM
    try:
        response = litellm.completion(
            model="gpt-4",  # Can be configured via environment variable
            messages=conversation_history,
            temperature=0.7,
            max_tokens=500
        )
        
        # Extract the response text
        response_text = response.choices[0].message.content
        
        # Add the assistant's response to the history
        assistant_message: AssistantMessage = {
            "role": "assistant",
            "content": response_text
        }
        conversation_history.append(assistant_message)
        
        # Save the updated conversation history
        save_result = save_conversation_history(
            user_id, 
            session_id, 
            conversation_history, 
            firebase_handler
        )
        
        if not save_result:
            logger.warning("Failed to save conversation history")
        
        return response_text, session_id
        
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return f"I'm sorry, I encountered an error: {str(e)}", session_id 