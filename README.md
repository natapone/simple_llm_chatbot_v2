# Simple LLM Chatbot v2

A pre-sales chatbot that engages with potential clients to collect lead information through natural conversation. The chatbot uses LangFlow for conversation flow, LiteLLM for language model integration, and Firebase for lead storage. Optimized for Python 3.11.

## Features

- Natural conversation flow with potential clients
- Progressive information gathering (business needs, timeline, budget)
- Contact information collection with consent
- Lead storage in Firebase Firestore
- Configurable system prompt without code changes
- Dynamic budget and timeline guidance stored in the database
- Python 3.11 compatibility with improved performance

## Project Structure

```
simple_llm_chatbot_v2/
├── app/                      # Main application code
│   ├── main.py               # FastAPI application
│   ├── langflow_handler.py   # LangFlow integration
│   ├── firebase_handler.py   # Firebase integration
│   ├── guidance_tools.py     # Budget and timeline guidance tools
│   └── config.py             # Configuration settings
├── static/                   # Simple CSS and JS files
├── templates/                # HTML template for chat interface
├── langflow/                 # LangFlow pipeline export
├── docs/                     # Documentation
│   ├── design/               # Design documentation
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

- [Setup Guide for Python 3.11](docs/usage/setup_guide.md)
- [API Documentation](docs/api/api_documentation.md)
- [System Prompt](docs/design/system_prompt.md)
- [LangFlow Pipeline](docs/design/langflow_pipeline.md)
- [Firebase Integration](docs/design/firebase_integration.md)
- [Dynamic Guidance Retrieval](docs/design/guidance_retrieval.md)
- [MVP Design](docs/design/mvp_design.md)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [LangFlow](https://github.com/langflow-ai/langflow)
- [LiteLLM](https://github.com/BerriAI/litellm)
- [Firebase](https://firebase.google.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
