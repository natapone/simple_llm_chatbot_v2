# Setup Guide

## Prerequisites
- Python 3.8 or higher
- Firebase account
- LangFlow (local installation or hosted instance)
- API key for an LLM provider (OpenAI, Anthropic, etc.)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/simple_llm_chatbot_v2.git
cd simple_llm_chatbot_v2
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Firebase Setup
1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Create a new project
3. Enable Firestore Database
4. Go to Project Settings > Service Accounts
5. Generate a new private key (this will download a JSON file)
6. Save the JSON file in a secure location

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
langflow run
```

### 2. Start the FastAPI Server
```bash
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
4. Save the pipeline

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

### Verifying Lead Storage
1. Go to the Firebase Console
2. Open your project
3. Go to Firestore Database
4. Check the "leads" collection for new entries

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

## Next Steps

After setting up the MVP, consider:
1. Customizing the system prompt to better match your business needs
2. Enhancing the chat interface with your branding
3. Adding more detailed lead information collection
4. Implementing analytics to track conversation effectiveness 