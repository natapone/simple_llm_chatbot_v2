# API Endpoints Documentation

This document provides detailed information about the API endpoints available in the Simple LLM Chatbot v2 application.

## Base URL

All endpoints are relative to the base URL of the server, which is typically:

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. However, each request should include a user ID to identify the user.

## Endpoints

### Chat Endpoint

Process a chat message and get a response from the chatbot.

**URL**: `/chat`

**Method**: `POST`

**Request Body**:

```json
{
  "user_id": "string",
  "message": "string",
  "session_id": "string | null"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `user_id` | string | Unique identifier for the user |
| `message` | string | The message content from the user |
| `session_id` | string or null | Session identifier for conversation context (optional) |

**Response**:

```json
{
  "response": "string",
  "session_id": "string",
  "timestamp": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `response` | string | The chatbot's response to the user's message |
| `session_id` | string | The session ID for the conversation (can be used in subsequent requests) |
| `timestamp` | string | ISO 8601 formatted timestamp of when the response was generated |

**Example Request**:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "message": "How much does it cost to build an e-commerce website?", "session_id": null}'
```

**Example Response**:

```json
{
  "response": "For an e-commerce website, the budget typically ranges from $5,000 to $15,000. This includes basic e-commerce functionality with product listings and payment processing. The actual cost may vary depending on specific requirements, complexity, and customization needs.",
  "session_id": "a0f81102-f44b-4038-bd03-8f71fd8eade1",
  "timestamp": "2025-03-06T01:10:57.967005+00:00"
}
```

### Web Interface

The chatbot also provides a web interface for easier interaction.

**URL**: `/`

**Method**: `GET`

**Response**: HTML page with the chat interface

### Leads Dashboard

View and manage leads collected from the chatbot.

**URL**: `/leads`

**Method**: `GET`

**Response**: HTML page with the leads dashboard

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK`: Request was successful
- `400 Bad Request`: Invalid request parameters
- `500 Internal Server Error`: Server-side error

Error responses include a JSON body with details:

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Rate Limiting

Currently, there are no rate limits implemented on the API endpoints.

## Data Types

### Chat Message

```typescript
{
  user_id: string;
  message: string;
  session_id?: string | null;
}
```

### Chat Response

```typescript
{
  response: string;
  session_id: string;
  timestamp: string;
}
```

### Lead Data

```typescript
{
  client_name: string | null;
  client_business: string | null;
  contact_information: string | null;
  project_description: string;
  features: string[];
  timeline: string | null;
  budget_range: string | null;
  confirmed_follow_up: boolean;
  timestamp: string;
}
```

## Future Endpoints

The following endpoints are planned for future releases:

- `/api/leads`: REST API for programmatically accessing lead data
- `/api/conversations`: REST API for accessing conversation history
- `/api/stats`: REST API for accessing usage statistics 