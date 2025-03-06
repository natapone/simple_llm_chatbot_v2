"""
Chat Handler Module

This module handles the processing of chat messages, including:
- Generating session IDs
- Storing conversation history
- Interacting with the LLM via LiteLLM
- Managing conversation context
- Integrating with the LangFlow pipeline

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
from app.database_handler import DatabaseHandler
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables - force reload to ensure we get the latest values
load_dotenv(override=True)

# Configure LiteLLM
api_key = os.getenv("LLM_API_KEY")
if not api_key:
    logger.error("LLM_API_KEY not found in environment variables!")
else:
    logger.info(f"API key loaded: {api_key[:5]}...{api_key[-4:]}")
    # Set the API key directly in the environment and for litellm
    os.environ["OPENAI_API_KEY"] = api_key
    litellm.api_key = api_key

# Set debug mode for more information
os.environ["LITELLM_LOG"] = "DEBUG"

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

class LLMHandler:
    """Handler for LLM interactions."""
    
    def __init__(self):
        """Initialize the LLM handler."""
        # Force reload environment variables
        load_dotenv(override=True)
        
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        self.provider = os.getenv("LLM_PROVIDER", "openai")
        self.temperature = 0.7
        self.max_tokens = 500
        
        # Get API key from environment
        self.api_key = os.getenv("LLM_API_KEY")
        if not self.api_key:
            logger.error("LLM_API_KEY not found in environment variables during LLMHandler initialization!")
        else:
            logger.info(f"LLMHandler initialized with API key: {self.api_key[:5]}...{self.api_key[-4:]}")
            # Set the API key directly in the environment
            os.environ["OPENAI_API_KEY"] = self.api_key
    
    def generate_response(
        self, 
        system_prompt: str, 
        user_message: str, 
        conversation_history: List[Message] = None
    ) -> str:
        """Generate a response using LiteLLM.
        
        Args:
            system_prompt: The system prompt.
            user_message: The user's message.
            conversation_history: The conversation history.
            
        Returns:
            The generated response text.
        """
        # Prepare messages for the LLM
        messages = []
        
        # Add system message
        system_message: SystemMessage = {
            "role": "system",
            "content": system_prompt
        }
        messages.append(system_message)
        
        # Add conversation history if provided
        if conversation_history:
            # Filter out system messages from history as we're adding our own
            filtered_history = [msg for msg in conversation_history if msg["role"] != "system"]
            messages.extend(filtered_history)
        
        # Add the current user message
        user_msg: UserMessage = {
            "role": "user",
            "content": user_message
        }
        messages.append(user_msg)
        
        # Generate response
        try:
            # Double-check API key before making the call
            if not self.api_key:
                # Try to reload from environment
                self.api_key = os.getenv("LLM_API_KEY")
                if not self.api_key:
                    raise ValueError("API key not found in environment variables")
                os.environ["OPENAI_API_KEY"] = self.api_key
            
            logger.info(f"Using API key for LLM call: {self.api_key[:5]}...{self.api_key[-4:]}")
            
            response = litellm.completion(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                api_key=self.api_key  # Explicitly pass the API key
            )
            
            # Extract the response text
            response_text = response.choices[0].message.content
            return response_text
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I'm sorry, I encountered an error. Please try again later."

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
    # Try to get the system prompt from the LangFlow pipeline
    try:
        from app.langflow.pipeline_config import SYSTEM_PROMPT
        return SYSTEM_PROMPT
    except ImportError:
        logger.warning("LangFlow pipeline not found, using default prompt")
        
        # Try to read from system_prompt.md file
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
    db_handler: DatabaseHandler
) -> List[Message]:
    """Get the conversation history for a user session.
    
    Args:
        user_id: The user's ID.
        session_id: The session ID.
        db_handler: The database handler instance.
        
    Returns:
        A list of message dictionaries representing the conversation history.
    """
    logger.info(f"Getting conversation history for user {user_id}, session {session_id}")
    
    # Get conversation from TinyDB
    conversation_data = db_handler.query_table(
        "conversations",
        "session_id",
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
    db_handler: DatabaseHandler
) -> bool:
    """Save the conversation history to TinyDB.
    
    Args:
        user_id: The user's ID.
        session_id: The session ID.
        messages: The list of message dictionaries.
        db_handler: The database handler instance.
        
    Returns:
        True if the save was successful, False otherwise.
    """
    logger.info(f"Saving conversation history for user {user_id}, session {session_id}")
    
    # Get current timestamp
    timestamp = datetime.now(pytz.UTC).isoformat()
    
    # Check if conversation already exists
    conversation_data = db_handler.query_table(
        "conversations",
        "session_id",
        session_id
    )
    
    if conversation_data and len(conversation_data) > 0:
        # Update existing conversation
        # TinyDB doesn't include the document ID in the query results by default
        # We need to use a different approach to get the document ID
        
        # Get all conversations
        all_conversations = db_handler.get_table_data("conversations")
        
        # Find the conversation with the matching session_id
        conversation_id = None
        for idx, conv in enumerate(all_conversations):
            if conv.get("session_id") == session_id:
                # In TinyDB, document IDs start at 1
                conversation_id = idx + 1
                break
        
        if conversation_id is not None:
            logger.info(f"Updating existing conversation with ID: {conversation_id}")
            return db_handler.update_document(
                "conversations",
                conversation_id,
                {
                    "messages": messages,
                    "updated_at": timestamp
                }
            )
        else:
            logger.warning(f"Could not find conversation ID for session {session_id}, creating new entry")
            # Fall through to create new conversation
    
    # Create new conversation
    conversation: ConversationHistory = {
        "user_id": user_id,
        "session_id": session_id,
        "messages": messages,
        "created_at": timestamp,
        "updated_at": timestamp
    }
    
    document_id = db_handler.add_document("conversations", conversation)
    return document_id > 0

def process_chat_message(
    user_id: str, 
    message: str, 
    session_id: Optional[str], 
    db_handler: DatabaseHandler
) -> Tuple[str, str]:
    """Process a chat message and generate a response.
    
    Args:
        user_id: The user's ID.
        message: The message from the user.
        session_id: The session ID, or None if this is a new session.
        db_handler: The database handler instance.
        
    Returns:
        A tuple containing (response_text, session_id).
    """
    logger.info(f"Processing message from user {user_id}")
    
    # Generate session ID if not provided
    if not session_id:
        session_id = generate_session_id()
        logger.info(f"Generated new session ID: {session_id}")
    
    # Get conversation history
    conversation_history = get_conversation_history(user_id, session_id, db_handler)
    
    try:
        # Use Langflow integration for processing the message
        from app.langflow.langflow_integration import LangFlowIntegration
        
        # Initialize the LangFlow integration
        langflow = LangFlowIntegration()
        logger.info("Using LangFlow integration for message processing")
        
        # Process the message through the LangFlow pipeline
        response_text, extracted_data = langflow.process_message(
            message=message,
            session_id=session_id,
            user_id=user_id,
            conversation_history=conversation_history
        )
        
        logger.info(f"Generated response via LangFlow: {response_text[:50]}...")
        logger.info(f"Extracted data: {extracted_data}")
        
        # Add the user message to the history
        user_message: UserMessage = {
            "role": "user",
            "content": message
        }
        conversation_history.append(user_message)
        
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
            db_handler
        )
        
        if not save_result:
            logger.warning("Failed to save conversation history")
        
        return response_text, session_id
        
    except Exception as e:
        logger.error(f"Error processing message with LangFlow: {str(e)}")
        logger.info("Falling back to direct LLM integration")
        
        # Fallback to direct LLM integration
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
        
        # Get LLM configuration from environment variables
        llm_model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")  # Use gpt-3.5-turbo as default
        llm_provider = os.getenv("LLM_PROVIDER", "openai")
        llm_api_key = os.getenv("LLM_API_KEY")
        
        # Log the API key (masked)
        masked_key = llm_api_key[:5] + "..." + llm_api_key[-4:] if llm_api_key and len(llm_api_key) > 10 else "None"
        logger.info(f"Using API key: {masked_key}")
        
        # Set the API key directly in the environment
        os.environ["OPENAI_API_KEY"] = llm_api_key
        
        # Generate response using LiteLLM
        try:
            logger.info(f"Calling LiteLLM with model: {llm_model}, provider: {llm_provider}")
            response = litellm.completion(
                model=llm_model,
                messages=conversation_history,
                temperature=0.7,
                max_tokens=500,
                api_key=llm_api_key  # Explicitly pass the API key
            )
            
            # Extract the response text
            response_text = response.choices[0].message.content
            logger.info(f"Generated response: {response_text[:50]}...")
            
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
                db_handler
            )
            
            if not save_result:
                logger.warning("Failed to save conversation history")
            
            return response_text, session_id
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I'm sorry, I encountered an error. Please try again later.", session_id 