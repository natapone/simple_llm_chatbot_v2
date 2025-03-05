# Pre-Sales Chatbot MVP Design

## Overview
This document outlines the design for the Minimum Viable Product (MVP) of our pre-sales chatbot. The chatbot is designed to engage with potential clients in a natural conversation, collect lead information, and store it in TinyDB for follow-up.

## Core Components

### 1. Chat Interface
A simple web-based chat interface that allows users to interact with the chatbot. The interface will:
- Display messages from both the user and the chatbot
- Provide a text input field for user messages
- Show a simple indicator when the chatbot is "typing"
- Maintain the conversation history during the session

### 2. Backend API
A Flask application that handles the chat interactions. The API will:
- Receive user messages via HTTP POST requests
- Process messages through the LangFlow pipeline
- Return chatbot responses
- Handle session management for conversation context
- Trigger lead storage in TinyDB when appropriate

### 3. LangFlow Pipeline
A conversation flow designed in LangFlow that orchestrates the chatbot's behavior. The pipeline will:
- Maintain the system prompt that guides the chatbot's behavior
- Process user messages and generate appropriate responses
- Extract lead information from the conversation
- Determine when to store lead data in TinyDB
- Follow a natural conversation flow similar to the example conversations

### 4. TinyDB Integration
A TinyDB database to store lead information. The integration will:
- Create a new document in a "leads" collection for each lead
- Store contact information, project requirements, budget, and timeline
- Only store information after receiving user consent for follow-up

## Data Flow

1. User sends a message through the chat interface
2. Message is sent to the backend API via HTTP POST
3. Backend passes the message to the LangFlow pipeline
4. LangFlow processes the message using the system prompt and LiteLLM
5. LangFlow generates a response and extracts any relevant lead information
6. If sufficient information is collected and user consent is given, data is stored in TinyDB
7. Response is returned to the frontend and displayed to the user

## Lead Data Structure

```json
{
  "timestamp": "2023-03-04T12:00:00Z",
  "client_name": "John Doe",
  "client_business": "Example Business",
  "contact_information": "john@example.com",
  "project_description": "E-commerce website",
  "features": ["Product listing", "Shopping cart", "Payment integration"],
  "timeline": "2 months",
  "budget_range": "$5,000",
  "confirmed_follow_up": true
}
```

## Conversation Flow

The chatbot will follow a natural conversation flow that:

1. Greets the user and asks about their business needs
2. Explores project requirements and features
3. Inquires about timeline expectations
4. Discusses budget considerations
5. Collects contact information
6. Confirms consent for follow-up
7. Closes the conversation with a thank you message

## System Prompt

The system prompt will guide the chatbot to:
- Maintain a friendly, helpful tone
- Ask questions progressively rather than all at once
- Provide reasonable estimates for timeline and budget based on project type
- Collect necessary lead information naturally throughout the conversation
- Ask for consent before storing contact information
- Handle uncertainty or vague responses gracefully

## Technical Considerations

### MVP Simplifications
- No user authentication
- System prompt stored directly in LangFlow
- Basic error handling
- Minimal logging
- No advanced frontend features

### Future Enhancements
- User authentication
- External prompt management
- Advanced analytics
- Integration with CRM systems
- Enhanced frontend features (typing indicators, read receipts, etc.)
- Multi-language support

## Implementation Timeline

1. **Setup (Day 1)**
   - Install dependencies
   - Set up project structure

2. **LangFlow Pipeline (Day 1-2)**
   - Create conversation flow
   - Configure system prompt
   - Test with example scenarios

3. **Backend (Day 2)**
   - Create Flask application
   - Implement chat endpoint
   - Connect to LangFlow and TinyDB

4. **Frontend (Day 3)**
   - Create HTML chat interface
   - Add JavaScript for message exchange
   - Style with CSS

5. **Testing and Refinement (Day 3-4)**
   - Test the full conversation flow
   - Make adjustments as needed
   - Ensure leads are properly stored 