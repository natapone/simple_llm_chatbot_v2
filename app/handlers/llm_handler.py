import os
import logging
from dotenv import load_dotenv
import litellm
from litellm import completion

class LLMHandler:
    """Handler for LLM interactions using LiteLLM."""
    
    def __init__(self):
        """Initialize the LLM handler with configuration from environment variables."""
        # Force reload environment variables
        load_dotenv(override=True)
        
        self.api_key = os.getenv("LLM_API_KEY")
        self.provider = os.getenv("LLM_PROVIDER", "openai")
        self.model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
        
        # Set the API key directly in the environment
        os.environ["OPENAI_API_KEY"] = self.api_key
        
        # Log configuration (with masked API key)
        masked_key = self.api_key[:5] + "..." + self.api_key[-4:] if self.api_key and len(self.api_key) > 10 else "None"
        logging.info(f"LLMHandler initialized with provider: {self.provider}, model: {self.model}, API key: {masked_key}")
        
        # Configure LiteLLM
        litellm.drop_params = True  # Prevents sending unnecessary parameters
        
    def get_completion(self, messages, temperature=0.7, max_tokens=1000):
        """Get a completion from the LLM.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Temperature for response generation (0.0 to 1.0)
            max_tokens: Maximum tokens in the response
            
        Returns:
            The LLM response text
        """
        try:
            # Log the request
            logging.info(f"Sending request to {self.provider}/{self.model} with {len(messages)} messages")
            
            # Make the completion request with explicit API key
            response = completion(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                api_key=self.api_key  # Explicitly pass the API key
            )
            
            # Extract and return the response text
            response_text = response.choices[0].message.content
            logging.info(f"Received response of {len(response_text)} characters")
            return response_text
            
        except Exception as e:
            logging.error(f"Error getting completion from LLM: {str(e)}")
            # Return a graceful error message
            return "I'm sorry, I encountered an error processing your request. Please try again later." 