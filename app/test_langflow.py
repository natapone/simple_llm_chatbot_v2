"""
Test script for the LangFlow pipeline.

This script tests the LangFlow pipeline by sending a test message and verifying the response.
"""

import os
import sys
import logging
from dotenv import load_dotenv
from unittest.mock import patch

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the LangFlow integration
from app.langflow.langflow_integration import LangFlowIntegration
from app.database_handler import DatabaseHandler

def test_langflow_pipeline():
    """Test the LangFlow pipeline."""
    logger.info("Testing LangFlow pipeline...")
    
    # Initialize the LangFlow integration
    langflow = LangFlowIntegration()
    
    # Test message
    test_message = "Hello, I'm interested in building an e-commerce website. Can you help me understand the costs and timeline?"
    
    # Test user and session IDs
    test_user_id = "test_user_123"
    test_session_id = "test_session_456"
    
    # Process the message
    response, extracted_data = langflow.process_message(
        message=test_message,
        session_id=test_session_id,
        user_id=test_user_id
    )
    
    # Log the response and extracted data
    logger.info(f"Response: {response}")
    logger.info(f"Extracted data: {extracted_data}")
    
    # Verify the response
    if response:
        logger.info("✅ LangFlow pipeline test passed!")
    else:
        logger.error("❌ LangFlow pipeline test failed!")

def test_project_type_detection():
    """Test the project type detection."""
    logger.info("Testing project type detection...")
    
    from app.langflow.pipeline_config import detect_project_type
    
    # Test conversation history
    test_conversation = [
        {"role": "user", "content": "I need an e-commerce website for my clothing store."},
        {"role": "assistant", "content": "I'd be happy to help with your e-commerce website."}
    ]
    
    # Detect project type
    project_type = detect_project_type(test_conversation)
    
    # Log the detected project type
    logger.info(f"Detected project type: {project_type}")
    
    # Verify the detection
    if project_type == "e-commerce":
        logger.info("✅ Project type detection test passed!")
    else:
        logger.error(f"❌ Project type detection test failed! Expected 'e-commerce', got '{project_type}'")

@patch('app.langflow.pipeline_config.extract_entity_with_llm')
def test_lead_extraction(mock_extract_entity):
    """Test the lead extraction."""
    logger.info("Testing lead extraction...")
    
    # Configure the mock to return specific values for different entity types
    def mock_extract_side_effect(conversation_text, entity_type):
        entity_values = {
            "client name": "John Smith",
            "business name": "Smith Clothing",
            "project description": "an e-commerce website for my clothing store",
            "project features": "product listings, shopping cart, payment processing",
            "project timeline": "2 months",
            "budget range": "around $10,000",
            "follow-up consent (yes/no)": "yes"
        }
        return entity_values.get(entity_type)
    
    mock_extract_entity.side_effect = mock_extract_side_effect
    
    from app.langflow.pipeline_config import extract_lead_information
    
    # Test conversation history
    test_conversation = [
        {"role": "user", "content": "My name is John Smith and I need an e-commerce website for my clothing store."},
        {"role": "assistant", "content": "I'd be happy to help with your e-commerce website."},
        {"role": "user", "content": "My budget is around $10,000 and I need it done in 2 months."},
        {"role": "assistant", "content": "That sounds reasonable for an e-commerce site."},
        {"role": "user", "content": "You can contact me at john@example.com for follow-up."},
        {"role": "assistant", "content": "Thank you for providing your contact information."}
    ]
    
    # Extract lead information
    lead_data = extract_lead_information(test_conversation)
    
    # Log the extracted lead information
    logger.info(f"Extracted lead information: {lead_data}")
    
    # Verify the extraction - updated to match actual extraction patterns
    expected_name = "John Smith"
    expected_business = "Smith Clothing"
    expected_email = "john@example.com"
    expected_budget = "around $10,000"
    expected_timeline = "2 months"
    
    # Check each field individually and log specific failures
    if lead_data.get("client_name") != expected_name:
        logger.error(f"❌ Name extraction failed! Expected '{expected_name}', got '{lead_data.get('client_name')}'")
    
    if lead_data.get("client_business") != expected_business:
        logger.error(f"❌ Business extraction failed! Expected '{expected_business}', got '{lead_data.get('client_business')}'")
    
    if lead_data.get("contact_information") != expected_email:
        logger.error(f"❌ Email extraction failed! Expected '{expected_email}', got '{lead_data.get('contact_information')}'")
    
    if lead_data.get("budget_range") != expected_budget:
        logger.error(f"❌ Budget extraction failed! Expected '{expected_budget}', got '{lead_data.get('budget_range')}'")
    
    if lead_data.get("timeline") != expected_timeline:
        logger.error(f"❌ Timeline extraction failed! Expected '{expected_timeline}', got '{lead_data.get('timeline')}'")
    
    # Overall test result
    if (lead_data.get("client_name") == expected_name and
        lead_data.get("client_business") == expected_business and
        lead_data.get("contact_information") == expected_email and
        lead_data.get("budget_range") == expected_budget and
        lead_data.get("timeline") == expected_timeline and
        lead_data.get("confirmed_follow_up") == True):
        logger.info("✅ Lead extraction test passed!")
    else:
        logger.error("❌ Lead extraction test failed!")

def main():
    """Run all tests."""
    logger.info("Starting LangFlow pipeline tests...")
    
    # Test the pipeline configuration
    try:
        from app.langflow.pipeline_config import create_langflow_pipeline
        pipeline = create_langflow_pipeline()
        if pipeline:
            logger.info("✅ Pipeline configuration test passed!")
        else:
            logger.error("❌ Pipeline configuration test failed!")
    except Exception as e:
        logger.error(f"❌ Pipeline configuration test failed: {str(e)}")
    
    # Test project type detection
    try:
        test_project_type_detection()
    except Exception as e:
        logger.error(f"❌ Project type detection test failed: {str(e)}")
    
    # Test lead extraction
    try:
        test_lead_extraction()
    except Exception as e:
        logger.error(f"❌ Lead extraction test failed: {str(e)}")
    
    # Test the full pipeline
    try:
        test_langflow_pipeline()
    except Exception as e:
        logger.error(f"❌ LangFlow pipeline test failed: {str(e)}")
    
    logger.info("LangFlow pipeline tests completed!")

if __name__ == "__main__":
    main() 