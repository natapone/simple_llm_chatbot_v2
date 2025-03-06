"""
Main Application Module

This module serves as the entry point for the FastAPI application.
It sets up the API routes and initializes the necessary components.

Optimized for Python 3.11 with enhanced typing features.
"""

import os
import logging
from typing import Dict, List, Any, Optional, Union, Annotated, TypedDict
from datetime import datetime, timedelta

import pytz
from fastapi import FastAPI, HTTPException, Depends, Request, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

# Use relative imports for app modules
from app.database_handler import DatabaseHandler
from app.chat_handler import process_chat_message

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

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

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

@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    """Root endpoint that serves the chat interface.
    
    Args:
        request: The incoming request.
        
    Returns:
        The HTML template for the chat interface.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/leads", response_class=HTMLResponse)
async def view_leads(request: Request) -> HTMLResponse:
    """Endpoint that serves the leads dashboard.
    
    Args:
        request: The incoming request.
        
    Returns:
        The HTML template for the leads dashboard.
    """
    # Get all leads from the database
    leads = db_handler.get_table_data("leads")
    
    # Convert to dictionary with lead_id as key
    leads_dict = {str(lead.doc_id): lead for lead in leads}
    
    # Count confirmed follow-ups
    confirmed_leads = sum(1 for lead in leads if lead.get('confirmed_follow_up', False))
    
    # Count recent leads (last 24 hours)
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    recent_leads = 0
    for lead in leads:
        try:
            timestamp_str = lead.get('timestamp', now.isoformat())
            # Handle different ISO format variations
            if 'Z' in timestamp_str:
                timestamp_str = timestamp_str.replace('Z', '+00:00')
            # Handle timestamps without timezone info
            if '+' not in timestamp_str and '-' not in timestamp_str[10:]:
                timestamp_str += '+00:00'
            lead_time = datetime.fromisoformat(timestamp_str)
            if lead_time > yesterday:
                recent_leads += 1
        except (ValueError, TypeError) as e:
            logger.warning(f"Error parsing timestamp: {e}")
            continue
    
    return templates.TemplateResponse(
        "leads.html", 
        {
            "request": request, 
            "leads": leads_dict,
            "confirmed_leads": confirmed_leads,
            "recent_leads": recent_leads
        }
    )

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
    uvicorn.run("app.main:app", host=host, port=port, reload=debug) 