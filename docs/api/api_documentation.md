# API Documentation

## Overview
This document describes the API endpoints for the pre-sales chatbot. The API is built using FastAPI and provides endpoints for chat interaction and session management.

## Base URL
For local development: `http://localhost:8000`

## Endpoints

### 1. Chat Endpoint

**URL**: `/chat`  
**Method**: `POST`  
**Description**: Send a message to the chatbot and receive a response.

#### Request Body
```json
{
  "message": "string",
  "session_id": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| message | string | The user's message to the chatbot |
| session_id | string | (Optional) A unique identifier for the conversation session. If not provided, a new session will be created. |

#### Response
```json
{
  "response": "string",
  "session_id": "string",
  "lead_stored": false
}
```

| Field | Type | Description |
|-------|------|-------------|
| response | string | The chatbot's response message |
| session_id | string | The session ID for the conversation |
| lead_stored | boolean | Indicates whether lead information was stored in Firebase |

#### Status Codes
- `200 OK`: Request successful
- `400 Bad Request`: Invalid request body
- `500 Internal Server Error`: Server error

#### Example
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hi, I need a website for my business", "session_id": "abc123"}'
```

### 2. Health Check Endpoint

**URL**: `/health`  
**Method**: `GET`  
**Description**: Check if the API is running.

#### Response
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

#### Status Codes
- `200 OK`: API is running

#### Example
```bash
curl -X GET "http://localhost:8000/health"
```

## Error Handling

### Error Response Format
```json
{
  "error": "string",
  "detail": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| error | string | A short error code or message |
| detail | string | A more detailed description of the error |

### Common Errors
- `invalid_request`: The request body is invalid or missing required fields
- `session_not_found`: The provided session ID does not exist
- `langflow_error`: Error communicating with LangFlow
- `firebase_error`: Error storing data in Firebase
- `server_error`: Unexpected server error

## Rate Limiting
For the MVP, no rate limiting is implemented. In production, consider adding rate limiting to prevent abuse.

## Authentication
For the MVP, no authentication is required. In production, consider adding API key authentication or other security measures.

## Future Endpoints

### Session Management
**URL**: `/sessions/{session_id}`  
**Method**: `GET`  
**Description**: Retrieve the conversation history for a session.

### Lead Retrieval
**URL**: `/leads`  
**Method**: `GET`  
**Description**: Retrieve stored leads from Firebase (admin access only). 