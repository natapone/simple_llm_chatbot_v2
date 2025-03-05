# API Documentation

## Overview

The Simple LLM Chatbot v2 provides a RESTful API for interacting with the chatbot. This document describes the available endpoints, request/response formats, and error handling.

## Base URL

All API endpoints are relative to the base URL of the server. By default, this is:

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. This may change in future versions.

## Endpoints

### GET /

Returns the chat interface HTML page.

#### Request

```http
GET / HTTP/1.1
Host: localhost:8000
```

#### Response

```http
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
...
</html>
```

### POST /chat

Processes a chat message and returns a response.

#### Request

```http
POST /chat HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "message": "Hello, I need help with a project",
  "session_id": "optional-session-id"
}
```

#### Request Parameters

| Parameter   | Type   | Required | Description                                                                                |
|-------------|--------|----------|--------------------------------------------------------------------------------------------|
| message     | string | Yes      | The user's message to the chatbot                                                          |
| session_id  | string | No       | A unique identifier for the conversation. If not provided, a new session ID will be generated |

#### Response

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "response": "Hi there! I'd be happy to help with your project. Could you tell me more about what you're looking to build?",
  "session_id": "generated-or-provided-session-id"
}
```

#### Response Parameters

| Parameter   | Type   | Description                                                |
|-------------|--------|------------------------------------------------------------|
| response    | string | The chatbot's response to the user's message               |
| session_id  | string | The session ID for the conversation (new or provided)      |

### Error Handling

The API uses standard HTTP status codes to indicate the success or failure of a request.

#### Common Error Codes

| Status Code | Description                                                         |
|-------------|---------------------------------------------------------------------|
| 400         | Bad Request - The request was malformed or missing required fields  |
| 500         | Internal Server Error - An error occurred while processing the request |

#### Error Response Format

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "detail": "Message field is required"
}
```

## Example Usage

### Python Example

```python
import requests

url = "http://localhost:8000/chat"
data = {
    "message": "Hello, I need help with a project",
    "session_id": "my-session-123"
}

response = requests.post(url, json=data)
result = response.json()

print(f"Chatbot: {result['response']}")
print(f"Session ID: {result['session_id']}")
```

### JavaScript Example

```javascript
async function sendMessage(message, sessionId = null) {
  const url = "http://localhost:8000/chat";
  const data = {
    message: message,
    session_id: sessionId
  };

  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  const result = await response.json();
  
  console.log(`Chatbot: ${result.response}`);
  console.log(`Session ID: ${result.session_id}`);
  
  return result;
}

// Usage
sendMessage("Hello, I need help with a project");
```

## Rate Limiting

Currently, there are no rate limits implemented. However, excessive requests may impact performance.

## Versioning

The current API version is v1. The API version is not included in the URL path but may be in future releases.

## Future Endpoints

The following endpoints are planned for future releases:

- `GET /conversations/{session_id}` - Retrieve the conversation history for a session
- `DELETE /conversations/{session_id}` - Delete a conversation
- `POST /admin/guidance` - Update guidance data (requires authentication) 