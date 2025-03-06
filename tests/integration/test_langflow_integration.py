"""
Integration tests for the LangFlow pipeline.

These tests verify that the application correctly interacts with LangFlow.
"""

import pytest
import os
import logging
from unittest.mock import patch
from pathlib import Path

# Import the LangFlow integration
from app.langflow.langflow_integration import LangFlowIntegration
from app.database_handler import DatabaseHandler
from app.langflow.pipeline_config import detect_project_type, extract_lead_information, create_langflow_pipeline

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TestLangFlowIntegration:
    """
    Integration tests for the LangFlow pipeline.
    """
    
    @pytest.fixture
    def langflow_integration(self):
        """Fixture for LangFlow integration."""
        return LangFlowIntegration()
    
    @pytest.fixture
    def test_user_id(self):
        """Fixture for test user ID."""
        return "test_user_123"
    
    @pytest.fixture
    def test_session_id(self):
        """Fixture for test session ID."""
        return "test_session_456"
    
    @pytest.fixture
    def test_db(self):
        """Fixture for test database."""
        # Create a temporary database for testing
        test_db_path = Path("tests/data/test_db.json")
        os.makedirs(test_db_path.parent, exist_ok=True)
        
        # Initialize the database handler
        db_handler = DatabaseHandler(str(test_db_path), initialize_default_data=True)
        
        yield db_handler
        
        # Clean up
        if test_db_path.exists():
            os.remove(test_db_path)
    
    def test_langflow_pipeline(self, langflow_integration, test_user_id, test_session_id):
        """Test the LangFlow pipeline."""
        # Test message
        test_message = "Hello, I'm interested in building an e-commerce website. Can you help me understand the costs and timeline?"
        
        # Process the message
        response, extracted_data = langflow_integration.process_message(
            message=test_message,
            session_id=test_session_id,
            user_id=test_user_id
        )
        
        # Verify the response
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_project_type_detection(self):
        """Test the project type detection."""
        # Test conversation history
        test_conversation = [
            {"role": "user", "content": "I need an e-commerce website for my clothing store."},
            {"role": "assistant", "content": "I'd be happy to help with your e-commerce website."}
        ]
        
        # Detect project type
        project_type = detect_project_type(test_conversation)
        
        # Verify the detection
        assert project_type == "e-commerce"
    
    @patch('app.langflow.pipeline_config.extract_entity_with_llm')
    def test_lead_extraction(self, mock_extract_entity):
        """Test the lead extraction."""
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
        
        # Verify the extraction
        assert lead_data.get("client_name") == "John Smith"
        assert lead_data.get("client_business") == "Smith Clothing"
        assert lead_data.get("project_description") == "an e-commerce website for my clothing store"
        assert lead_data.get("budget_range") == "around $10,000"
        assert lead_data.get("timeline") == "2 months"
        assert lead_data.get("confirmed_follow_up") == True
    
    def test_pipeline_configuration(self):
        """Test the pipeline configuration."""
        # Create the pipeline
        pipeline = create_langflow_pipeline()
        
        # Verify the pipeline
        assert pipeline is not None
        assert isinstance(pipeline, dict)
        assert "nodes" in pipeline
        assert "edges" in pipeline 