# Setup Guide for Python 3.11

## Prerequisites
- Python 3.11
- Firebase account
- LangFlow (local installation or hosted instance)
- API key for an LLM provider (OpenAI, Anthropic, etc.)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/simple_llm_chatbot_v2.git
cd simple_llm_chatbot_v2
```

### 2. Create a Virtual Environment with Python 3.11
```bash
# Check your Python version first
python --version

# If you have multiple Python versions, specify Python 3.11
python3.11 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

### 3. Install Dependencies
```bash
# Upgrade pip to the latest version
pip install --upgrade pip

# Install the required packages
pip install -r requirements.txt
```

### 4. Firebase Setup
1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Create a new project
3. Enable Firestore Database
4. Go to Project Settings > Service Accounts
5. Generate a new private key (this will download a JSON file)
6. Save the JSON file in a secure location

#### 4.1 Firebase Collections
The application uses the following collections in Firestore:
- **leads**: Stores lead information collected from conversations
- **budget_guidance**: Stores budget ranges for different project types
- **timeline_guidance**: Stores timeline estimates for different project types

These collections will be automatically initialized with default data when the application starts.

### 5. Environment Variables
Create a `.env` file in the root directory with the following variables:
```
FIREBASE_CREDENTIALS_PATH=/path/to/your/firebase-credentials.json
LANGFLOW_API_URL=http://localhost:7860/api/v1/predict  # If using local LangFlow
LLM_API_KEY=your_llm_api_key
LLM_PROVIDER=openai  # or anthropic, etc.
```

## Running the Application

### 1. Start LangFlow (if using local installation)
```bash
# Make sure you're in your virtual environment
langflow run
```

### 2. Start the FastAPI Server
```bash
# Make sure you're in your virtual environment
cd app
uvicorn main:app --reload
```

### 3. Access the Chat Interface
Open your browser and go to:
```
http://localhost:8000
```

## LangFlow Pipeline Setup

### 1. Import the Pipeline
1. Open LangFlow in your browser (typically at http://localhost:7860)
2. Click on "Import"
3. Select the JSON file from the `langflow` directory

### 2. Configure the Pipeline
1. Update the LiteLLM node with your API key and provider
2. Verify the Firebase connection node has the correct path to your credentials
3. Review the system prompt and make any desired changes
4. Ensure the guidance tools are properly registered
5. Save the pipeline

### 3. Export the Updated Pipeline
1. Click on "Export"
2. Save the JSON file to the `langflow` directory

## Testing the Chatbot

### Example Conversation
Try the following conversation to test the chatbot:
```
User: Hi, I need a website for my business.
Bot: [Greeting and question about business type]
User: I run a small clothing store, and I want to sell online.
Bot: [Question about features]
...
```

### Testing Budget and Timeline Guidance
To test the dynamic guidance retrieval:
```
User: How much would an e-commerce website cost?
Bot: [Retrieves and displays budget guidance for e-commerce sites]
User: How long would it take to build?
Bot: [Retrieves and displays timeline guidance for e-commerce sites]
```

### Verifying Lead Storage
1. Go to the Firebase Console
2. Open your project
3. Go to Firestore Database
4. Check the "leads" collection for new entries

## Updating Guidance Data

To update the budget or timeline guidance:

1. Go to the Firebase Console
2. Open your project
3. Go to Firestore Database
4. Navigate to the `budget_guidance` or `timeline_guidance` collection
5. Edit the documents to update the values
6. The changes will be reflected immediately in the chatbot's responses

## Python 3.11 Specific Notes

### Package Compatibility
Python 3.11 offers improved performance and error messages compared to earlier versions. All the packages in `requirements.txt` have been tested with Python 3.11.

### Dependency Management
If you encounter any package compatibility issues with Python 3.11, try the following:
```bash
# Update a specific package to its latest version
pip install --upgrade package_name

# If a package fails to install, try installing its dependencies first
pip install package_dependencies
pip install package_name
```

### Type Hints
The codebase uses type hints that are fully compatible with Python 3.11's typing system, including the newer typing features.

## Troubleshooting

### Common Issues

#### Firebase Connection Error
- Verify the path to your Firebase credentials is correct
- Check that the credentials have the necessary permissions
- Ensure the Firestore database is enabled in your Firebase project

#### LangFlow Connection Error
- Verify the LangFlow API URL is correct
- Check that LangFlow is running
- Ensure the pipeline is properly configured

#### LLM API Error
- Verify your API key is correct
- Check that you have sufficient credits/quota with your LLM provider
- Ensure the LLM provider is correctly specified

#### Guidance Retrieval Error
- Check that the `budget_guidance` and `timeline_guidance` collections exist in Firestore
- Verify that the collections contain the expected documents
- Ensure the guidance tools are properly registered in LangFlow

#### Python 3.11 Specific Issues
- If you see "ModuleNotFoundError", ensure all dependencies are installed: `pip install -r requirements.txt`
- For "SyntaxError" messages, check that all code is compatible with Python 3.11
- If you encounter performance issues, ensure you're using the latest version of Python 3.11.x

## Next Steps

After setting up the MVP, consider:
1. Customizing the system prompt to better match your business needs
2. Enhancing the chat interface with your branding
3. Adding more detailed lead information collection
4. Implementing analytics to track conversation effectiveness
5. Adding more project types to the guidance collections 