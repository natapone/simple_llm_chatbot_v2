# Testing Documentation

## Overview

This document outlines the testing strategy and procedures for the Simple LLM Chatbot v2. The testing approach includes unit tests, integration tests, and end-to-end tests to ensure the reliability and functionality of the system.

## Testing Tools

- **pytest**: Primary testing framework
- **pytest-cov**: For test coverage reporting
- **httpx**: For testing FastAPI endpoints
- **unittest.mock**: For mocking dependencies

## Test Directory Structure

```
/tests
├── unit/
│   ├── test_chat_handler.py
│   ├── test_database_handler.py
│   └── test_guidance_tools.py
├── integration/
│   ├── test_database_integration.py
│   └── test_llm_integration.py
├── e2e/
│   └── test_chat_flow.py
└── conftest.py
```

## Unit Tests

Unit tests focus on testing individual components in isolation, with dependencies mocked as needed.

### Chat Handler Tests

Tests for the `chat_handler.py` module, including:

- Session ID generation
- Conversation history management
- Message formatting
- LLM interaction (mocked)

### Database Handler Tests

Tests for the `database_handler.py` module, including:

- Document retrieval
- Table querying
- Document creation/updating/deletion
- Error handling
- Database initialization
- Backup functionality

### Guidance Tools Tests

Tests for the `guidance_tools.py` module, including:

- Budget guidance retrieval and formatting
- Timeline guidance retrieval and formatting
- Error handling
- Type checking with Python 3.11 features

## Integration Tests

Integration tests focus on testing the interaction between components.

### Database Integration Tests

Tests for the integration with TinyDB, including:

- Real database operations (using a temporary test database)
- Data storage and retrieval
- Query functionality
- Database persistence
- Error handling

### LLM Integration Tests

Tests for the integration with LiteLLM, including:

- Real LLM connection (using a test API key)
- Message processing
- Response handling
- Error handling

## End-to-End Tests

End-to-end tests focus on testing the complete system from user input to response.

### Chat Flow Tests

Tests for the complete chat flow, including:

- API endpoint testing
- Conversation flow
- Session management
- Database interaction
- Error handling

## Test Coverage

The goal is to maintain at least 80% test coverage for all components. Coverage reports can be generated using:

```bash
pytest --cov=app tests/
```

## Test Environment

Tests should be run in a dedicated test environment with:

- A temporary TinyDB database
- Test API keys
- Mocked external services where appropriate

## Continuous Integration

Tests should be run automatically on each pull request and before each deployment using a CI/CD pipeline.

## Test Data

Test data should be stored in the `/tests/data` directory and should include:

- Sample chat messages
- Sample database documents
- Sample LLM responses

## Writing Tests

### Test Naming Convention

Test functions should follow the naming convention:

```
test_<function_name>_<scenario>
```

For example:
- `test_generate_session_id_valid`
- `test_get_document_not_found`

### Test Structure

Each test should follow the Arrange-Act-Assert pattern:

1. **Arrange**: Set up the test data and environment
2. **Act**: Call the function being tested
3. **Assert**: Verify the results

Example:

```python
def test_generate_session_id_valid():
    # Arrange
    chat_handler = ChatHandler()
    
    # Act
    session_id = chat_handler.generate_session_id()
    
    # Assert
    assert isinstance(session_id, str)
    assert len(session_id) > 0
```

## Running Tests

### Running All Tests

```bash
pytest
```

### Running Specific Test Categories

```bash
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run end-to-end tests
pytest tests/e2e/
```

### Running Tests with Coverage

```bash
pytest --cov=app tests/
```

## Test Reports

Test reports should be generated and stored for each test run. The reports should include:

- Test results (pass/fail)
- Test coverage
- Test duration

## Troubleshooting Tests

Common issues and their solutions:

- **Database Connection Issues**: Ensure the test database path is valid and the directory is writable
- **LLM API Issues**: Ensure the test LLM API key is valid and has sufficient quota
- **Timeout Issues**: Increase the timeout for tests that interact with external services

## Mocking Strategy

External dependencies should be mocked in unit tests to ensure tests are fast and reliable. The mocking strategy includes:

- **TinyDB**: Mock the TinyDB instance and responses
- **LLM**: Mock the LiteLLM client and responses
- **External APIs**: Mock any external API calls

Example:

```python
@patch('app.chat_handler.litellm.completion')
def test_process_message(mock_completion):
    # Set up mock response
    mock_completion.return_value = {
        'choices': [{'message': {'content': 'Mock response'}}]
    }
    
    # Test code here
```

## Test Fixtures

Common test fixtures should be defined in `conftest.py` to be reused across tests. Examples include:

- TinyDB fixture with temporary database
- LLM client fixture
- Sample data fixtures

Example:

```python
@pytest.fixture
def temp_db_path():
    """Create a temporary directory for the test database."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = os.path.join(temp_dir, "test_db.json")
        yield db_path

@pytest.fixture
def db_handler(temp_db_path):
    """Create a DatabaseHandler instance with a temporary database."""
    handler = DatabaseHandler(temp_db_path)
    yield handler
```

## Testing Database Operations

When testing database operations:

1. Use a temporary database file for each test
2. Initialize the database with known test data
3. Perform operations and verify results
4. Clean up the temporary database after the test

Example:

```python
def test_add_document(db_handler):
    # Arrange
    table_name = "test_table"
    data = {"name": "Test Document", "value": 42}
    
    # Act
    doc_id = db_handler.add_document(table_name, data)
    
    # Assert
    assert doc_id is not None
    retrieved = db_handler.get_document(table_name, doc_id)
    assert retrieved is not None
    assert retrieved["name"] == "Test Document"
    assert retrieved["value"] == 42
```

## Testing Guidance Tools

When testing guidance tools:

1. Mock the database handler to return known test data
2. Test both specific project type queries and all-types queries
3. Verify formatting functions produce expected output
4. Test error handling for missing or invalid data

## Testing Chat Flow

When testing the complete chat flow:

1. Set up a test client for the FastAPI application
2. Use a temporary database for the test
3. Send test messages and verify responses
4. Check that data is correctly stored in the database
5. Verify session management works correctly 