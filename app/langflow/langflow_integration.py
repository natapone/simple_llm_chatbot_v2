"""
LangFlow Integration Module

This module provides integration between the LangFlow pipeline and the chat handler.
It handles the communication with the LangFlow API and processes the responses.
"""

import os
import json
import requests
from typing import Dict, Any, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LangFlowIntegration:
    """Integration with LangFlow API for processing chat messages."""
    
    def __init__(self, api_url: Optional[str] = None):
        """Initialize the LangFlow integration.
        
        Args:
            api_url: URL of the LangFlow API. If None, it will be read from the environment.
        """
        self.api_url = api_url or os.getenv("LANGFLOW_API_URL", "http://localhost:7860/api/v1/predict")
        self.pipeline_path = os.path.join(os.path.dirname(__file__), "pipeline.json")
        self.pipeline = self._load_pipeline()
        logger.info(f"LangFlow integration initialized with API URL: {self.api_url}")
    
    def _load_pipeline(self) -> Dict[str, Any]:
        """Load the pipeline configuration from the JSON file.
        
        Returns:
            The pipeline configuration as a dictionary
        """
        try:
            with open(self.pipeline_path, "r") as f:
                pipeline = json.load(f)
            logger.info(f"Pipeline loaded from {self.pipeline_path}")
            return pipeline
        except Exception as e:
            logger.error(f"Error loading pipeline: {str(e)}")
            # Return a minimal pipeline if the file cannot be loaded
            return {"nodes": [], "edges": []}
    
    def process_message(self, message: str, session_id: str, user_id: str, conversation_history: List[Dict[str, Any]] = None) -> Tuple[str, Dict[str, Any]]:
        """Process a message through the LangFlow pipeline.
        
        Args:
            message: The user's message
            session_id: The session ID for the conversation
            user_id: The user ID
            conversation_history: The conversation history
            
        Returns:
            A tuple containing the response and any extracted data
        """
        # In a real implementation, this would send the message to the LangFlow API
        # For now, we'll simulate the response using LiteLLM directly
        
        try:
            # Prepare the request payload
            payload = {
                "input": message,
                "session_id": session_id,
                "user_id": user_id,
                "chat_history": conversation_history or []
            }
            
            # Check if we should use the actual LangFlow API
            use_langflow_api = os.getenv("USE_LANGFLOW_API", "False").lower() == "true"
            
            if use_langflow_api:
                # Send the request to the LangFlow API
                logger.info(f"Sending request to LangFlow API at {self.api_url}")
                response = requests.post(self.api_url, json=payload)
                
                if response.status_code != 200:
                    logger.error(f"Error from LangFlow API: {response.status_code} - {response.text}")
                    raise Exception(f"LangFlow API returned status code {response.status_code}")
                
                response_data = response.json()
                response_text = response_data.get("response", "")
                logger.info(f"Received response from LangFlow API: {response_text[:50]}...")
                
                # Extract any additional data from the response
                extracted_data = response_data.get("extracted_data", {})
            else:
                # Simulate the LangFlow pipeline locally
                logger.info("Simulating LangFlow pipeline locally")
                
                # Detect project type
                from app.langflow.pipeline_config import detect_project_type
                project_type = detect_project_type(conversation_history or [] + [
                    {"role": "user", "content": message}
                ])
                logger.info(f"Detected project type: {project_type}")
                
                # Check if the message is asking about budget or timeline
                message_lower = message.lower()
                
                # Check for budget-related questions
                is_budget_question = any(keyword in message_lower for keyword in [
                    "budget", "cost", "price", "pricing", "how much", "expensive", "cheap", "afford"
                ])
                
                # Check for timeline-related questions
                is_timeline_question = any(keyword in message_lower for keyword in [
                    "timeline", "time", "duration", "how long", "schedule", "deadline", "when"
                ])
                
                # Handle budget questions
                if is_budget_question:
                    logger.info("Budget question detected, using get_budget_guidance tool")
                    from app.guidance_tools import get_budget_guidance, format_budget_guidance
                    
                    # Get budget guidance
                    budget_guidance = get_budget_guidance(project_type)
                    
                    # Format the guidance
                    budget_info = format_budget_guidance(budget_guidance)
                    
                    # Generate a response that incorporates the budget information
                    system_prompt = f"""
                    You are a helpful pre-sales assistant. The user has asked about budget information.
                    Use the following budget information in your response:
                    
                    {budget_info}
                    
                    Be friendly and helpful. If the user has asked about a specific project type that isn't covered in the budget information,
                    explain that you don't have specific information for that project type but can provide general guidance.
                    """
                    
                    # Create a new LLM handler for this specific response
                    from app.chat_handler import LLMHandler
                    llm_handler = LLMHandler()
                    response_text = llm_handler.generate_response(
                        system_prompt=system_prompt,
                        user_message=message,
                        conversation_history=conversation_history or []
                    )
                    
                # Handle timeline questions
                elif is_timeline_question:
                    logger.info("Timeline question detected, using get_timeline_guidance tool")
                    from app.guidance_tools import get_timeline_guidance, format_timeline_guidance
                    
                    # Get timeline guidance
                    timeline_guidance = get_timeline_guidance(project_type)
                    
                    # Format the guidance
                    timeline_info = format_timeline_guidance(timeline_guidance)
                    
                    # Generate a response that incorporates the timeline information
                    system_prompt = f"""
                    You are a helpful pre-sales assistant. The user has asked about timeline information.
                    Use the following timeline information in your response:
                    
                    {timeline_info}
                    
                    Be friendly and helpful. If the user has asked about a specific project type that isn't covered in the timeline information,
                    explain that you don't have specific information for that project type but can provide general guidance.
                    """
                    
                    # Create a new LLM handler for this specific response
                    from app.chat_handler import LLMHandler
                    llm_handler = LLMHandler()
                    response_text = llm_handler.generate_response(
                        system_prompt=system_prompt,
                        user_message=message,
                        conversation_history=conversation_history or []
                    )
                    
                # Handle other questions with standard LLM response
                else:
                    # Generate a response using the LLM
                    from app.chat_handler import LLMHandler
                    llm_handler = LLMHandler()
                    
                    system_prompt = self._get_system_prompt()
                    response_text = llm_handler.generate_response(
                        system_prompt=system_prompt,
                        user_message=message,
                        conversation_history=conversation_history or []
                    )
            
            # Extract lead information from the conversation
            from app.langflow.pipeline_config import extract_lead_information
            lead_data = extract_lead_information(conversation_history or [] + [
                {"role": "user", "content": message},
                {"role": "assistant", "content": response_text}
            ])
            
            # Detect project type (again, to ensure we have it after the response)
            from app.langflow.pipeline_config import detect_project_type
            project_type = detect_project_type(conversation_history or [] + [
                {"role": "user", "content": message},
                {"role": "assistant", "content": response_text}
            ])
            
            # Store lead if appropriate
            from app.langflow.pipeline_config import store_lead
            if lead_data.get("confirmed_follow_up") and lead_data.get("client_name") and lead_data.get("contact_information"):
                lead_id = store_lead(lead_data)
                logger.info(f"Lead stored with ID: {lead_id}")
            
            # Store conversation
            from app.langflow.pipeline_config import store_conversation
            conversation_id = store_conversation(
                conversation_history or [] + [
                    {"role": "user", "content": message},
                    {"role": "assistant", "content": response_text}
                ],
                session_id=session_id,
                user_id=user_id
            )
            logger.info(f"Conversation stored with ID: {conversation_id}")
            
            # Return the response and extracted data
            return response_text, {
                "lead_data": lead_data,
                "project_type": project_type
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return "I'm sorry, I encountered an error processing your message. Please try again later.", {}
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt from the pipeline configuration.
        
        Returns:
            The system prompt as a string
        """
        # In a real implementation, this would extract the system prompt from the pipeline
        # For now, we'll use the one from the pipeline_config module
        from app.langflow.pipeline_config import SYSTEM_PROMPT
        return SYSTEM_PROMPT 