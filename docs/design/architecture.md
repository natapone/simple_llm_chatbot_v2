# Chatbot Architecture

This document outlines the architecture of the Simple LLM Chatbot v2, explaining the key components and their interactions.

## System Overview

The Simple LLM Chatbot v2 is a pre-sales assistant designed to provide information about software development services, collect lead information, and assist potential clients with budget and timeline guidance. The system is built with a modular architecture to ensure maintainability, scalability, and extensibility.

## Architecture Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Web Interface  │◄────┤  FastAPI Server │◄────┤  Chat Handler   │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  TinyDB         │◄────┤  Database       │◄────┤  LangFlow       │
│  Database       │     │  Handler        │     │  Integration    │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │                 │
                                                │  LLM Handler    │
                                                │  (LiteLLM)      │
                                                │                 │
                                                └─────────────────┘
```

## Core Components

### 1. Web Interface

**Purpose**: Provides a user-friendly interface for interacting with the chatbot.

**Key Files**:
- `app/templates/index.html`: Main chat interface
- `app/templates/leads.html`: Leads dashboard
- `app/static/css/style.css`: Styling for the chat interface
- `app/static/css/leads.css`: Styling for the leads dashboard
- `app/static/js/chat.js`: Client-side JavaScript for the chat interface

**Features**:
- Real-time chat interface
- Message history display
- Typing indicators
- Navigation to leads dashboard
- Mobile-responsive design

### 2. FastAPI Server

**Purpose**: Handles HTTP requests and serves the web interface.

**Key Files**:
- `app/main.py`: FastAPI application entry point

**Endpoints**:
- `GET /`: Serves the chat interface
- `POST /chat`: Processes chat messages
- `GET /leads`: Serves the leads dashboard

**Features**:
- Request validation using Pydantic models
- Error handling with custom exception handlers
- CORS support for cross-origin requests
- Static file serving
- Template rendering with Jinja2

### 3. Chat Handler

**Purpose**: Processes chat messages and manages conversation flow.

**Key Files**:
- `app/chat_handler.py`: Main chat handling logic

**Key Functions**:
- `process_chat_message()`: Processes user messages and generates responses
- `save_conversation_history()`: Saves conversation history to the database
- `get_conversation_history()`: Retrieves conversation history from the database
- `generate_session_id()`: Generates unique session IDs for conversations
- `get_system_prompt()`: Retrieves the system prompt for the LLM

### 4. LangFlow Integration

**Purpose**: Integrates with LangFlow for advanced conversation processing.

**Key Files**:
- `app/langflow/langflow_integration.py`: LangFlow integration logic
- `app/langflow/pipeline_config.py`: LangFlow pipeline configuration

**Key Functions**:
- `process_message()`: Processes messages through the LangFlow pipeline
- `detect_project_type()`: Detects the type of project being discussed
- `extract_lead_information()`: Extracts lead information from conversations

### 5. LLM Handler

**Purpose**: Interfaces with language models via LiteLLM.

**Key Files**:
- `app/chat_handler.py`: Contains the LLMHandler class

**Key Functions**:
- `generate_response()`: Generates responses using the LLM
- `format_messages()`: Formats messages for the LLM API

### 6. Database Handler

**Purpose**: Manages TinyDB database operations.

**Key Files**:
- `app/database_handler.py`: TinyDB integration logic

**Key Functions**:
- `add_document()`: Adds documents to the database
- `update_document()`: Updates existing documents
- `get_document()`: Retrieves documents by ID
- `query_table()`: Queries tables based on field values
- `store_lead()`: Stores lead information

### 7. Guidance Tools

**Purpose**: Provides budget and timeline guidance for different project types.

**Key Files**:
- `app/guidance_tools.py`: Budget and timeline guidance tools

**Key Functions**:
- `get_budget_guidance()`: Retrieves budget guidance for project types
- `get_timeline_guidance()`: Retrieves timeline guidance for project types
- `format_budget_guidance()`: Formats budget guidance for presentation
- `format_timeline_guidance()`: Formats timeline guidance for presentation

## Data Flow

1. **User Interaction**:
   - User sends a message through the web interface
   - JavaScript sends a POST request to the `/chat` endpoint

2. **Message Processing**:
   - FastAPI server receives the request
   - Request is validated using Pydantic models
   - `process_chat_message()` is called with the user's message

3. **Conversation Processing**:
   - LangFlow integration processes the message
   - Project type is detected
   - If the message is about budget or timeline, guidance tools are used
   - Lead information is extracted if provided

4. **Response Generation**:
   - LLM generates a response based on the processed message
   - Response is formatted and returned to the user
   - Conversation history is saved to the database

5. **Lead Management**:
   - Extracted lead information is stored in the database
   - Leads can be viewed in the leads dashboard

## Database Schema

### Tables

1. **conversations**:
   - `user_id`: String
   - `session_id`: String
   - `messages`: List of message objects
   - `created_at`: Timestamp
   - `updated_at`: Timestamp

2. **leads**:
   - `client_name`: String (optional)
   - `client_business`: String (optional)
   - `contact_information`: String (optional)
   - `project_description`: String
   - `features`: List of strings
   - `timeline`: String (optional)
   - `budget_range`: String (optional)
   - `confirmed_follow_up`: Boolean
   - `timestamp`: Timestamp

3. **budget_guidance**:
   - `project_type`: String
   - `min_budget`: Integer
   - `max_budget`: Integer
   - `description`: String (optional)

4. **timeline_guidance**:
   - `project_type`: String
   - `min_timeline`: String
   - `max_timeline`: String
   - `description`: String (optional)

## Error Handling

The system implements comprehensive error handling:

1. **API Errors**:
   - Custom exception handlers for different error types
   - Structured error responses with appropriate HTTP status codes

2. **LLM Errors**:
   - Fallback to direct LLM integration if LangFlow fails
   - Retry logic for transient errors
   - Timeout handling for long-running requests

3. **Database Errors**:
   - Error logging for database operations
   - Graceful handling of database connection issues
   - Data validation before storage

## Security Considerations

1. **Input Validation**:
   - All user inputs are validated using Pydantic models
   - Sanitization of inputs to prevent injection attacks

2. **API Key Management**:
   - API keys are stored in environment variables
   - Keys are not exposed in logs or responses

3. **Data Protection**:
   - Sensitive data is not logged
   - Database file is excluded from version control

## Performance Optimizations

1. **LLM Usage**:
   - Efficient prompt design to minimize token usage
   - Caching of common responses
   - Fallback to simpler models for basic queries

2. **Database Operations**:
   - Efficient query patterns
   - Indexing for frequently queried fields
   - Batch operations where appropriate

## Future Enhancements

1. **Authentication**:
   - User authentication system
   - Role-based access control

2. **Multi-language Support**:
   - Support for multiple languages
   - Language detection

3. **Analytics Dashboard**:
   - Usage statistics
   - Conversation analytics
   - Lead conversion tracking

4. **CRM Integration**:
   - Integration with popular CRM systems
   - Automated lead follow-up 