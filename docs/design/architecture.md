# Simple LLM Chatbot v2 - Architecture

## Overview

The Simple LLM Chatbot v2 is designed as a modular system with several key components that work together to provide a seamless chat experience. The architecture follows a clean separation of concerns, with each component responsible for a specific aspect of the system.

## System Components

### 1. FastAPI Backend (`main.py`)

The FastAPI backend serves as the entry point for the application, handling HTTP requests and responses. It provides the following endpoints:

- `GET /`: Serves the chat interface
- `POST /chat`: Processes chat messages and returns responses

The backend is responsible for:
- Initializing the application
- Setting up CORS middleware
- Configuring logging
- Defining API routes
- Handling exceptions

### 2. Chat Handler (`chat_handler.py`)

The Chat Handler is responsible for processing chat messages and generating responses. It:

- Manages conversation history
- Generates session IDs
- Interacts with the LLM via LiteLLM
- Stores conversation data in TinyDB
- Retrieves system prompts
- Formats messages for the LLM

### 3. Database Handler (`database_handler.py`)

The Database Handler provides an interface to TinyDB, allowing the application to:

- Retrieve documents
- Query collections
- Add new documents
- Update existing documents
- Delete documents
- Perform batch operations

### 4. Guidance Tools (`guidance_tools.py`)

The Guidance Tools module provides functions for retrieving and formatting budget and timeline guidance from the TinyDB database. These tools are used by the LLM to provide accurate information to users.

### 5. LangFlow Pipeline (`/app/langflow`)

The LangFlow pipeline defines the conversation flow and logic. It:

- Structures the conversation
- Integrates with the guidance tools
- Manages the conversation state
- Handles different conversation paths

### 6. Frontend (`/app/templates`, `/app/static`)

The frontend provides a user interface for interacting with the chatbot. It includes:

- HTML templates
- CSS styles
- JavaScript for handling user interactions
- WebSocket connection for real-time chat

## Data Flow

1. User sends a message through the chat interface
2. The message is sent to the FastAPI backend via a POST request
3. The backend passes the message to the Chat Handler
4. The Chat Handler processes the message and sends it to the LLM
5. The LLM generates a response, potentially using the Guidance Tools
6. The response is sent back to the user through the FastAPI backend
7. The conversation history is stored in TinyDB

## System Architecture Diagram

```
+----------------+     +----------------+     +----------------+
|                |     |                |     |                |
|  Chat Interface|---->|  FastAPI       |---->|  Chat Handler  |
|  (Frontend)    |<----|  Backend       |<----|                |
|                |     |                |     |                |
+----------------+     +----------------+     +-------+--------+
                                                     |
                                                     v
+----------------+     +----------------+     +----------------+
|                |     |                |     |                |
|  TinyDB        |<----|  Guidance      |<----|  LLM           |
|  Database      |---->|  Tools         |---->|  (via LiteLLM) |
|                |     |                |     |                |
+----------------+     +----------------+     +----------------+
                              ^
                              |
                       +------+--------+
                       |               |
                       |  LangFlow     |
                       |  Pipeline     |
                       |               |
                       +---------------+
```

## Security Considerations

- Environment variables are used for sensitive information
- Input validation is performed on all user inputs
- Error handling prevents information leakage
- Local database reduces external attack vectors

## Scalability

The system is designed to be scalable:

- Stateless backend allows for horizontal scaling
- TinyDB can be replaced with a more robust database if needed
- LiteLLM supports multiple LLM providers
- Modular design allows for component replacement

## Future Enhancements

- User authentication
- Admin dashboard
- Analytics integration
- Multi-language support
- Enhanced error handling
- Performance optimizations
- Migration to a more robust database if needed 