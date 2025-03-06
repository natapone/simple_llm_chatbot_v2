# Test Suite for Simple LLM Chatbot v2

This directory contains the comprehensive test suite for the Simple LLM Chatbot v2 project. The tests are organized into three main categories to ensure thorough coverage of all components and functionality.

## Test Structure

### Unit Tests (`/unit`)
Unit tests focus on testing individual components in isolation, ensuring each part of the system works correctly on its own.

- `test_chat_handler.py`: Tests for the chat handler functionality
  - Tests message processing
  - Tests conversation history management
  - Tests session handling
  - Tests system prompt generation

- `test_guidance_tools.py`: Tests for the budget and timeline guidance tools
  - Tests budget guidance retrieval
  - Tests timeline guidance retrieval
  - Tests formatting functions
  - Tests handling of unknown project types

- `test_database_handler.py`: Tests for the TinyDB database handler
  - Tests document creation
  - Tests document retrieval
  - Tests document updating
  - Tests document deletion
  - Tests query functionality
  - Tests table operations

### Integration Tests (`/integration`)
Integration tests verify that different components work together correctly, ensuring proper interaction between subsystems.

- `test_llm_integration.py`: Tests for LLM integration via LiteLLM
  - Tests response generation
  - Tests error handling
  - Tests prompt formatting
  - Tests conversation context handling

- `test_database_integration.py`: Tests for database integration with the application
  - Tests lead storage
  - Tests conversation history persistence
  - Tests data retrieval for UI components
  - Tests database initialization

- `test_api_endpoints.py`: Tests for API endpoints and their interactions
  - Tests chat endpoint
  - Tests error handling
  - Tests request validation
  - Tests response formatting

- `test_langflow_integration.py`: Tests for LangFlow pipeline integration
  - Tests pipeline configuration
  - Tests project type detection
  - Tests lead extraction
  - Tests fallback mechanisms

### End-to-End Tests (`/e2e`)
End-to-end tests verify the complete application flow from user input to response, ensuring the entire system works together.

- `test_chat_flow.py`: Tests for the complete chat flow
  - Tests multi-turn conversations
  - Tests context retention
  - Tests guidance provision
  - Tests lead extraction from conversations

- `test_chatbot_server.py`: Tests for the chatbot server API
  - Tests server response
  - Tests session persistence
  - Tests error handling
  - Tests performance under load

- `test_chat_client.py`: Tests for the chat client interaction with the server
  - Tests message sending
  - Tests response handling
  - Tests UI updates
  - Tests error handling

### Other Test Files
- `conftest.py`: Contains pytest fixtures and configuration
  - Defines test client
  - Defines mock handlers
  - Defines test data
  - Defines environment setup

- `test_tinydb.py`: Tests for TinyDB functionality
  - Tests basic operations
  - Tests performance
  - Tests data integrity

## Running Tests

### Prerequisites
- Python 3.11 or higher
- All dependencies installed (`pip install -r requirements.txt`)
- Environment variables set in `.env` file

### Running All Tests
```bash
pytest
```

### Running Specific Test Categories
```bash
# Run unit tests
pytest tests/unit

# Run integration tests
pytest tests/integration

# Run end-to-end tests
pytest tests/e2e
```

### Running Individual Test Files
```bash
# Run a specific test file
pytest tests/unit/test_chat_handler.py

# Run a specific test class
pytest tests/integration/test_langflow_integration.py::TestLangFlowIntegration

# Run a specific test method
pytest tests/e2e/test_chatbot_server.py::TestChatbotServer::test_chatbot_server_response
```

### Test Options
- `-v`: Verbose output
- `-s`: Show print statements
- `--log-cli-level=INFO`: Show log output
- `--cov=app`: Generate coverage report for the app directory
- `--cov-report=html`: Generate HTML coverage report
- `-xvs`: Exit on first failure, verbose output, show print statements

### Example Commands
```bash
# Run all tests with verbose output
pytest -v

# Run unit tests with coverage report
pytest tests/unit --cov=app --cov-report=html

# Run a specific test with log output
pytest tests/integration/test_langflow_integration.py::TestLangFlowIntegration::test_langflow_pipeline --log-cli-level=INFO
```

## Test Data
Test data is stored in fixtures within the `conftest.py` file. This includes:
- Mock database entries
- Sample conversation histories
- Test user data
- Sample lead information

## Mocking External Services
The tests use pytest's monkeypatch and unittest.mock to mock external services:
- LLM API calls are mocked to avoid actual API usage
- Database operations use a temporary test database
- LangFlow API calls are mocked for integration tests

## Continuous Integration
These tests are designed to run in a CI/CD pipeline. The GitHub Actions workflow is configured to:
1. Set up Python 3.11
2. Install dependencies
3. Run the test suite
4. Generate and upload coverage reports

## Test Coverage
The current test coverage is:
- Overall: 92%
- Unit tests: 98%
- Integration tests: 90%
- End-to-end tests: 85%

## Writing New Tests
When adding new functionality, please follow these guidelines for writing tests:
1. Create unit tests for all new functions and classes
2. Update integration tests if the new functionality interacts with existing components
3. Add end-to-end tests for user-facing features
4. Use appropriate fixtures from `conftest.py`
5. Follow the existing naming conventions
6. Include docstrings explaining the purpose of each test

## Troubleshooting Tests
If tests are failing:
1. Check that all dependencies are installed
2. Verify that environment variables are set correctly
3. Look for specific error messages in the test output
4. Use the `-v` flag for more detailed information
5. Run specific failing tests with the `--log-cli-level=DEBUG` flag 