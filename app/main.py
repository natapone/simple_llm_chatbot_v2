"""
Main Application Module

This module serves as the entry point for the FastAPI application.
It sets up the API routes and initializes the necessary components.

Optimized for Python 3.11 with enhanced typing features.
"""

import os
import logging
from typing import Dict, List, Any, Optional, Union, Annotated, TypedDict
from datetime import datetime

import pytz
from fastapi import FastAPI, HTTPException, Depends, Request, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from database_handler import DatabaseHandler
from chat_handler import process_chat_message

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Pre-Sales Chatbot API",
    description="API for the pre-sales chatbot that provides information about services and pricing",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize TinyDB
tinydb_path = os.getenv('TINYDB_PATH', './data/chatbot_db.json')
if not tinydb_path:
    logger.error("TINYDB_PATH environment variable not set, using default path")
    tinydb_path = './data/chatbot_db.json'

db_handler = DatabaseHandler(tinydb_path)
logger.info(f"TinyDB initialized at {tinydb_path}")

class ChatMessage(BaseModel):
    """Chat message model for request validation."""
    user_id: str = Field(..., description="Unique identifier for the user")
    message: str = Field(..., description="The message content from the user")
    session_id: Optional[str] = Field(None, description="Session identifier for conversation context")

class ChatResponse(TypedDict):
    """Type definition for chat response data."""
    response: str
    session_id: str
    timestamp: str

@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint that returns a welcome message.
    
    Returns:
        A dictionary with a welcome message.
    """
    return {"message": "Welcome to the Pre-Sales Chatbot API"}

@app.post("/chat", response_model=Dict[str, Any])
async def chat(
    chat_message: Annotated[ChatMessage, Body(...)],
) -> ChatResponse:
    """Process a chat message from a user.
    
    Args:
        chat_message: The chat message from the user.
        
    Returns:
        A dictionary containing the chatbot's response, session ID, and timestamp.
        
    Raises:
        HTTPException: If there is an error processing the message.
    """
    try:
        logger.info(f"Received message from user {chat_message.user_id}")
        
        # Process the message
        response, session_id = process_chat_message(
            user_id=chat_message.user_id,
            message=chat_message.message,
            session_id=chat_message.session_id,
            db_handler=db_handler
        )
        
        # Get current timestamp
        timestamp = datetime.now(pytz.UTC).isoformat()
        
        return {
            "response": response,
            "session_id": session_id,
            "timestamp": timestamp
        }
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat message: {str(e)}"
        )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for the application.
    
    Args:
        request: The request that caused the exception.
        exc: The exception that was raised.
        
    Returns:
        A JSON response with the error details.
    """
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"An unexpected error occurred: {str(exc)}"}
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("DEBUG", "False").lower() == "true"
    uvicorn.run("main:app", host=host, port=port, reload=debug) 