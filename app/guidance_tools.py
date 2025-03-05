"""
Guidance Tools Module

This module provides tools for retrieving budget and timeline guidance
from the TinyDB database. These tools are used by the LLM to provide
up-to-date information to users about project costs and timelines.

Optimized for Python 3.11 with enhanced typing features.
"""

import os
from typing import List, Dict, Optional, Any, Union, TypedDict, NotRequired
from database_handler import DatabaseHandler

class BudgetGuidance(TypedDict):
    """Type definition for budget guidance data."""
    project_type: str
    min_budget: int
    max_budget: int
    description: NotRequired[str]

class TimelineGuidance(TypedDict):
    """Type definition for timeline guidance data."""
    project_type: str
    min_timeline: str
    max_timeline: str
    description: NotRequired[str]

def get_budget_guidance(project_type: Optional[str] = None) -> List[BudgetGuidance]:
    """Get budget guidance for a specific project type or all types.
    
    Args:
        project_type: The type of project to get guidance for.
            If None, returns guidance for all project types.
            
    Returns:
        A list of budget guidance dictionaries.
    """
    db_handler = DatabaseHandler(os.getenv('TINYDB_PATH', './data/chatbot_db.json'))
    
    if project_type:
        # Get guidance for specific project type
        guidance = db_handler.query_table(
            'budget_guidance', 
            'project_type', 
            project_type
        )
    else:
        # Get all guidance
        guidance = db_handler.get_table_data('budget_guidance')
    
    return guidance

def get_timeline_guidance(project_type: Optional[str] = None) -> List[TimelineGuidance]:
    """Get timeline guidance for a specific project type or all types.
    
    Args:
        project_type: The type of project to get guidance for.
            If None, returns guidance for all project types.
            
    Returns:
        A list of timeline guidance dictionaries.
    """
    db_handler = DatabaseHandler(os.getenv('TINYDB_PATH', './data/chatbot_db.json'))
    
    if project_type:
        # Get guidance for specific project type
        guidance = db_handler.query_table(
            'timeline_guidance', 
            'project_type', 
            project_type
        )
    else:
        # Get all guidance
        guidance = db_handler.get_table_data('timeline_guidance')
    
    return guidance

def format_budget_guidance(guidance: List[BudgetGuidance]) -> str:
    """Format budget guidance data for presentation to the user.
    
    Args:
        guidance: A list of budget guidance dictionaries.
        
    Returns:
        Formatted budget guidance text.
    """
    if not guidance:
        return "I'm sorry, I don't have specific budget information available at the moment."
    
    formatted_text = "Here's some guidance on project budgets:\n\n"
    
    for item in guidance:
        formatted_text += f"- {item['project_type']}: ${item['min_budget']:,}-${item['max_budget']:,}\n"
        if 'description' in item and item['description']:
            formatted_text += f"  ({item['description']})\n"
    
    return formatted_text

def format_timeline_guidance(guidance: List[TimelineGuidance]) -> str:
    """Format timeline guidance data for presentation to the user.
    
    Args:
        guidance: A list of timeline guidance dictionaries.
        
    Returns:
        Formatted timeline guidance text.
    """
    if not guidance:
        return "I'm sorry, I don't have specific timeline information available at the moment."
    
    formatted_text = "Here's some guidance on project timelines:\n\n"
    
    for item in guidance:
        formatted_text += f"- {item['project_type']}: {item['min_timeline']} to {item['max_timeline']}\n"
        if 'description' in item and item['description']:
            formatted_text += f"  ({item['description']})\n"
    
    return formatted_text

# Note: The initialize_guidance_data function is no longer needed here
# as the DatabaseHandler class now handles initialization of default data 