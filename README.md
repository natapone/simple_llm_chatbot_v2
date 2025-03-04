# Simple LLM Chatbot v2

A pre-sales chatbot that engages with potential clients to collect lead information through natural conversation. The chatbot uses LangFlow for conversation flow, LiteLLM for language model integration, and Firebase for lead storage. Optimized for Python 3.11.

## Project Status

✅ **Design Phase Complete** - The project is now ready for development.

## Features

- Natural conversation flow with potential clients
- Progressive information gathering (business needs, timeline, budget)
- Contact information collection with consent
- Lead storage in Firebase Firestore
- Configurable system prompt without code changes
- Dynamic budget and timeline guidance stored in the database
- Python 3.11 compatibility with improved performance
- Handling of both standard and non-standard project types

## Project Structure

```
simple_llm_chatbot_v2/
├── app/                      # Main application code
│   ├── main.py               # FastAPI application
│   ├── langflow_handler.py   # LangFlow integration
│   ├── firebase_handler.py   # Firebase integration
│   ├── guidance_tools.py     # Budget and timeline guidance tools
│   ├── chat_handler.py       # Chat processing logic
│   └── config.py             # Configuration settings
├── static/                   # Simple CSS and JS files
├── templates/                # HTML template for chat interface
├── langflow/                 # LangFlow pipeline export
├── docs/                     # Documentation
│   ├── design/               # Design documentation
│   │   ├── README.md                 # Design overview
│   │   ├── mvp_design.md             # MVP design overview
│   │   ├── conversation_flow.md      # Detailed conversation flow
│   │   ├── data_schema.md            # Firebase data schema
│   │   ├── firebase_integration.md   # Firebase setup and integration
│   │   ├── guidance_retrieval.md     # Dynamic guidance tools
│   │   ├── system_prompt.md          # LLM system prompt
│   │   └── langflow_pipeline.md      # LangFlow pipeline design
│   ├── development/          # Development documentation
│   │   ├── README.md                 # Development guide
│   │   └── python311_typing.md       # Python 3.11 typing features
│   ├── api/                  # API documentation
│   └── usage/                # Usage guides
├── .env.example              # Example environment variables
├── .gitignore                # Git ignore file
├── project_info.txt          # Project information and changelog
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Getting Started

### Prerequisites

- Python 3.11
- Firebase account
- LangFlow (local installation or hosted instance)
- API key for an LLM provider (OpenAI, Anthropic, etc.)

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/simple_llm_chatbot_v2.git
   cd simple_llm_chatbot_v2
   ```

2. Create a virtual environment with Python 3.11
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. Install dependencies
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Set up Firebase (see docs/usage/setup_guide.md for detailed instructions)

5. Create a `.env` file with your configuration (see .env.example)

### Running the Application

1. Start LangFlow (if using local installation)
   ```bash
   langflow run
   ```

2. Start the FastAPI server
   ```bash
   cd app
   uvicorn main:app --reload
   ```

3. Access the chat interface at http://localhost:8000

## Documentation

The project includes comprehensive documentation organized into several categories to help developers understand, implement, and maintain the system.

### Documentation Categories

#### 1. Design Documentation
Design documentation outlines the architecture, data structures, conversation flow, and implementation details for the chatbot system.

**Key Documents:**
- [Design Overview](docs/design/README.md)
- [MVP Design](docs/design/mvp_design.md)
- [Conversation Flow](docs/design/conversation_flow.md)
- [Data Schema](docs/design/data_schema.md)
- [Firebase Integration](docs/design/firebase_integration.md)
- [Guidance Retrieval](docs/design/guidance_retrieval.md)
- [System Prompt](docs/design/system_prompt.md)
- [LangFlow Pipeline](docs/design/langflow_pipeline.md)

#### 2. Development Documentation
Development documentation provides guidance for developers implementing the system, including coding standards, best practices, and implementation details.

**Key Documents:**
- [Development Guide](docs/development/README.md)
- [Python 3.11 Typing Features](docs/development/python311_typing.md)

#### 3. API Documentation
API documentation describes the endpoints, request/response formats, and error handling for the chatbot's API.

**Key Documents:**
- [API Documentation](docs/api/api_documentation.md)

#### 4. Usage Documentation
Usage documentation provides instructions for setting up, configuring, and using the chatbot system.

**Key Documents:**
- [Setup Guide for Python 3.11](docs/usage/setup_guide.md)

### Documentation Standards

All documentation follows these standards:

1. **Markdown Format**: All documentation is written in Markdown for easy viewing on GitHub and other platforms.
2. **Comprehensive Coverage**: Each document covers a specific aspect of the system in detail.
3. **Code Examples**: Where appropriate, documentation includes code examples to illustrate concepts.
4. **Diagrams**: Complex concepts are illustrated with diagrams (ASCII or embedded images).
5. **Cross-References**: Documents reference each other where relevant to provide a cohesive understanding.

### Using This Documentation

- **New Developers**: Start with the [Design Overview](docs/design/README.md) and [Development Guide](docs/development/README.md)
- **Implementation**: Refer to specific design documents for detailed implementation guidance
- **Setup**: Follow the [Setup Guide](docs/usage/setup_guide.md) for environment setup
- **API Integration**: Use the [API Documentation](docs/api/api_documentation.md) for integrating with the chatbot

## Development Roadmap

1. **Core Components Implementation**
   - Firebase Handler
   - Guidance Tools
   - Chat Handler

2. **LangFlow Pipeline Setup**
   - Create pipeline based on design
   - Test with example conversations

3. **FastAPI Backend Development**
   - Implement chat endpoint
   - Connect to LangFlow and Firebase

4. **Frontend Implementation**
   - Create chat interface
   - Implement message exchange

5. **Testing and Refinement**
   - Unit and integration tests
   - End-to-end testing
   - Performance optimization

## Maintaining the Project

When making changes to the codebase:

1. Update relevant documentation to reflect the changes
2. Add new documentation for new features or components
3. Keep the changelog in `project_info.txt` up to date
4. Ensure code examples in documentation remain accurate

## Future Enhancements

As the project evolves, additional features and documentation will be added:

- User authentication for admin access
- Advanced analytics for conversation effectiveness
- Integration with CRM systems
- Multi-language support
- Enhanced frontend features
- User guides for administrators
- Deployment guides for production environments
- Performance tuning recommendations
- Troubleshooting guides

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [LangFlow](https://github.com/langflow-ai/langflow)
- [LiteLLM](https://github.com/BerriAI/litellm)
- [Firebase](https://firebase.google.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
