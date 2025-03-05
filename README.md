# Simple LLM Chatbot v2

A simple chatbot implementation using LiteLLM for LLM integration, TinyDB for data storage, and FastAPI for the backend. The chatbot provides responses based on user queries and can access guidance tools for budget and timeline information.

## Features

- Chat interface for user interaction
- LLM integration via LiteLLM
- TinyDB integration for local data storage
- Dynamic guidance tools for budget and timeline information
- LangFlow pipeline for conversation flow

## Requirements

- Python 3.11
- LLM API key (OpenAI, Anthropic, etc.)

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd simple_llm_chatbot_v2
   ```

2. Create a virtual environment:
   ```
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file with your LLM API key and other settings.

5. Initialize the database:
   ```
   python app/db_init.py
   ```
   This will create the database file with initial seed data from `data/seed_data.json`. The script:
   - Reads seed data from `data/seed_data.json`
   - Creates the database file at the path specified in `.env` (default: `./data/chatbot_db.json`)
   - Initializes the database with the seed data
   - If the database file already exists, it will be removed and recreated

6. Run the application:
   ```
   cd app
   uvicorn main:app --reload
   ```

7. Access the application at `http://localhost:8000`

## Project Structure

- `/app`: Main application code
  - `main.py`: FastAPI application entry point
  - `chat_handler.py`: Handles chat processing and LLM integration
  - `database_handler.py`: TinyDB integration for data storage
  - `guidance_tools.py`: Tools for retrieving budget and timeline guidance
  - `db_init.py`: Database initialization script
  - `/langflow`: LangFlow pipeline implementation
  - `/static`: Frontend assets (CSS, JS, images)
  - `/templates`: Frontend HTML templates
- `/data`: Data files
  - `seed_data.json`: Initial seed data for the database
- `/docs`: Project documentation
- `/venv`: Python virtual environment (Python 3.11)

## Database Management

The project uses TinyDB for local data storage. The database file is not included in version control to prevent conflicts and unnecessary commits. Instead, a seed data file (`data/seed_data.json`) is provided with initial data.

To initialize or reset the database:
```
python app/db_init.py
```

For production deployments, set the `TINYDB_PATH` environment variable to specify a different database location.

## Documentation

For more detailed documentation, see the `/docs` directory:

- `/docs/design`: Design documentation
- `/docs/api`: API documentation
- `/docs/test`: Test documentation

## License

[MIT License](LICENSE)
