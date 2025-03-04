"""
Guidance Tools Module

This module provides tools for retrieving budget and timeline guidance
from the Firebase database. These tools are used by the LLM to provide
up-to-date information to users about project costs and timelines.

Optimized for Python 3.11 with enhanced typing features.
"""

import os
from typing import List, Dict, Optional, Any, Union, TypedDict, NotRequired
from firebase_handler import FirebaseHandler

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
    firebase_handler = FirebaseHandler(os.getenv('FIREBASE_CREDENTIALS_PATH'))
    
    if project_type:
        # Get guidance for specific project type
        guidance = firebase_handler.query_collection(
            'budget_guidance', 
            field='project_type', 
            operator='==', 
            value=project_type
        )
    else:
        # Get all guidance
        guidance = firebase_handler.get_collection_data('budget_guidance')
    
    return guidance

def get_timeline_guidance(project_type: Optional[str] = None) -> List[TimelineGuidance]:
    """Get timeline guidance for a specific project type or all types.
    
    Args:
        project_type: The type of project to get guidance for.
            If None, returns guidance for all project types.
            
    Returns:
        A list of timeline guidance dictionaries.
    """
    firebase_handler = FirebaseHandler(os.getenv('FIREBASE_CREDENTIALS_PATH'))
    
    if project_type:
        # Get guidance for specific project type
        guidance = firebase_handler.query_collection(
            'timeline_guidance', 
            field='project_type', 
            operator='==', 
            value=project_type
        )
    else:
        # Get all guidance
        guidance = firebase_handler.get_collection_data('timeline_guidance')
    
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

def initialize_guidance_data(firebase_handler: FirebaseHandler) -> None:
    """Initialize budget and timeline guidance data if not already present.
    
    Args:
        firebase_handler: An initialized FirebaseHandler instance.
    """
    # Check if budget data already exists
    budget_data = firebase_handler.get_collection_data('budget_guidance')
    if not budget_data:
        # Initialize budget guidance
        budget_guidance: List[BudgetGuidance] = [
            {
                "project_type": "Basic website",
                "min_budget": 1500,
                "max_budget": 3000,
                "description": "Simple informational website with a few pages"
            },
            {
                "project_type": "E-commerce site",
                "min_budget": 3000,
                "max_budget": 8000,
                "description": "Online store with product listings and payment processing"
            },
            {
                "project_type": "Mobile app",
                "min_budget": 5000,
                "max_budget": 15000,
                "description": "Native or cross-platform mobile application"
            },
            {
                "project_type": "Custom software",
                "min_budget": 10000,
                "max_budget": 50000,
                "description": "Bespoke software solution for specific business needs"
            }
        ]
        
        for guidance in budget_guidance:
            firebase_handler.db.collection('budget_guidance').add(guidance)
    
    # Check if timeline data already exists
    timeline_data = firebase_handler.get_collection_data('timeline_guidance')
    if not timeline_data:
        # Initialize timeline guidance
        timeline_guidance: List[TimelineGuidance] = [
            {
                "project_type": "Basic website",
                "min_timeline": "2 weeks",
                "max_timeline": "4 weeks",
                "description": "Simple informational website with a few pages"
            },
            {
                "project_type": "E-commerce site",
                "min_timeline": "1 month",
                "max_timeline": "3 months",
                "description": "Online store with product listings and payment processing"
            },
            {
                "project_type": "Mobile app",
                "min_timeline": "2 months",
                "max_timeline": "4 months",
                "description": "Native or cross-platform mobile application"
            },
            {
                "project_type": "Custom software",
                "min_timeline": "3 months",
                "max_timeline": "6 months",
                "description": "Bespoke software solution for specific business needs"
            }
        ]
        
        for guidance in timeline_guidance:
            firebase_handler.db.collection('timeline_guidance').add(guidance) 