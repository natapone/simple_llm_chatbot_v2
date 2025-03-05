#!/usr/bin/env python3
"""
Database initialization script.

This script initializes the TinyDB database with seed data from data/seed_data.json.
It should be run once during initial setup or when resetting the database.
"""

import os
import json
import logging
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the parent directory to sys.path to allow importing from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database_handler import DatabaseHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def init_database():
    """Initialize the database with seed data."""
    # Load environment variables
    load_dotenv()
    
    # Get database path from environment variable or use default
    db_path = os.getenv("TINYDB_PATH", "./data/chatbot_db.json")
    seed_data_path = "./data/seed_data.json"
    
    # Convert to absolute paths for clarity in logging
    abs_db_path = os.path.abspath(db_path)
    abs_seed_data_path = os.path.abspath(seed_data_path)
    
    logger.info(f"Database path: {abs_db_path}")
    logger.info(f"Seed data path: {abs_seed_data_path}")
    
    # Create directory if it doesn't exist
    db_dir = os.path.dirname(db_path)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        logger.info(f"Created directory: {db_dir}")
    
    # Check if seed data exists
    if not os.path.exists(seed_data_path):
        logger.error(f"Seed data file not found: {seed_data_path}")
        return False
    
    try:
        # Load seed data
        with open(seed_data_path, 'r') as f:
            seed_data = json.load(f)
            logger.info(f"Loaded seed data from {seed_data_path}")
        
        # Remove existing database file if it exists
        if os.path.exists(db_path):
            os.remove(db_path)
            logger.info(f"Removed existing database at {db_path}")
        
        # Initialize database handler with initialize_default_data=False
        # to prevent duplicate data since we're adding seed data manually
        db_handler = DatabaseHandler(db_path, initialize_default_data=False)
        logger.info(f"Initialized DatabaseHandler with path: {db_path}")
        
        # Insert seed data into tables
        for table_name, table_data in seed_data.items():
            logger.info(f"Adding data to table '{table_name}' with {len(table_data)} documents")
            for doc_id, doc_data in table_data.items():
                result = db_handler.add_document(table_name, doc_data)
                logger.info(f"Added document to {table_name} with ID: {result}")
        
        # Verify database file was created
        if os.path.exists(db_path):
            logger.info(f"Database file created successfully at {db_path}")
        else:
            logger.error(f"Database file was not created at {db_path}")
            return False
        
        logger.info(f"Database initialized successfully at {db_path}")
        return True
    
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = init_database()
    if success:
        logger.info("Database initialization completed successfully")
    else:
        logger.error("Database initialization failed") 