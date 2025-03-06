"""
LangFlow Pipeline Package

This package contains the LangFlow pipeline configuration and integration for the pre-sales chatbot.
"""

from app.langflow.pipeline_config import (
    detect_project_type,
    extract_lead_information,
    store_lead,
    store_conversation,
    create_langflow_pipeline,
    save_pipeline_config,
    SYSTEM_PROMPT
)

from app.langflow.langflow_integration import LangFlowIntegration

__all__ = [
    'LangFlowIntegration',
    'detect_project_type',
    'extract_lead_information',
    'store_lead',
    'store_conversation',
    'create_langflow_pipeline',
    'save_pipeline_config',
    'SYSTEM_PROMPT'
] 