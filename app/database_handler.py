"""
Database Handler for Simple LLM Chatbot v2

This module provides a DatabaseHandler class for interacting with TinyDB,
which stores lead information, budget guidance, and timeline guidance data.
"""

from tinydb import TinyDB, Query, where
import os
import datetime
import logging
from typing import Dict, List, Any, Optional, Union

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DatabaseHandler:
    """Handler for TinyDB database operations."""
    
    def __init__(self, db_path: str, initialize_default_data: bool = True):
        """Initialize TinyDB connection.
        
        Args:
            db_path: Path to the TinyDB JSON file.
            initialize_default_data: Whether to initialize default data if tables are empty.
        """
        logger.info(f"Initializing DatabaseHandler with path: {db_path}")
        
        # Store the database path
        self.db_path = db_path
        
        # Ensure directory exists
        try:
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            logger.info(f"Ensured directory exists for database at: {os.path.dirname(db_path)}")
        except Exception as e:
            logger.error(f"Failed to create directory for database: {str(e)}")
            raise
        
        try:
            self.db = TinyDB(db_path)
            logger.info("TinyDB database initialized successfully")
            
            # Initialize tables
            self.leads_table = self.db.table('leads')
            self.budget_guidance_table = self.db.table('budget_guidance')
            self.timeline_guidance_table = self.db.table('timeline_guidance')
            
            # Initialize default data if tables are empty and initialization is requested
            if initialize_default_data:
                self._initialize_default_data()
        except Exception as e:
            logger.error(f"Failed to initialize TinyDB: {str(e)}")
            raise
    
    def _initialize_default_data(self):
        """Initialize default data in tables if they are empty."""
        # Initialize budget guidance if empty
        if not self.budget_guidance_table.all():
            logger.info("Initializing default budget guidance data")
            default_budget_data = [
                {
                    "project_type": "e-commerce",
                    "min_budget": 5000,
                    "max_budget": 15000,
                    "description": "Basic e-commerce website with product listings and payment processing"
                },
                {
                    "project_type": "corporate",
                    "min_budget": 3000,
                    "max_budget": 10000,
                    "description": "Professional corporate website with company information and contact forms"
                },
                {
                    "project_type": "blog",
                    "min_budget": 2000,
                    "max_budget": 5000,
                    "description": "Blog website with content management system"
                }
            ]
            for data in default_budget_data:
                self.budget_guidance_table.insert(data)
        
        # Initialize timeline guidance if empty
        if not self.timeline_guidance_table.all():
            logger.info("Initializing default timeline guidance data")
            default_timeline_data = [
                {
                    "project_type": "e-commerce",
                    "min_timeline": "6 weeks",
                    "max_timeline": "3 months",
                    "description": "Development timeline for a standard e-commerce website"
                },
                {
                    "project_type": "corporate",
                    "min_timeline": "4 weeks",
                    "max_timeline": "2 months",
                    "description": "Development timeline for a corporate website"
                },
                {
                    "project_type": "blog",
                    "min_timeline": "2 weeks",
                    "max_timeline": "1 month",
                    "description": "Development timeline for a blog website"
                }
            ]
            for data in default_timeline_data:
                self.timeline_guidance_table.insert(data)
    
    def get_document(self, table_name: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a document by ID from a specific table.
        
        Args:
            table_name: Name of the table to query
            doc_id: ID of the document to retrieve
            
        Returns:
            The document if found, None otherwise
        """
        logger.info(f"Getting document with ID {doc_id} from table {table_name}")
        try:
            table = self.db.table(table_name)
            doc_id_int = int(doc_id) if doc_id.isdigit() else doc_id
            doc = table.get(doc_id=doc_id_int)
            
            if doc:
                logger.info(f"Document found: {doc}")
            else:
                logger.info(f"No document found with ID {doc_id} in table {table_name}")
                
            return doc
        except Exception as e:
            logger.error(f"Error getting document: {str(e)}")
            return None
    
    def get_table_data(self, table_name: str) -> List[Dict[str, Any]]:
        """Get all documents from a specific table.
        
        Args:
            table_name: Name of the table to query
            
        Returns:
            List of all documents in the table
        """
        logger.info(f"Getting all documents from table {table_name}")
        try:
            table = self.db.table(table_name)
            docs = table.all()
            logger.info(f"Retrieved {len(docs)} documents from table {table_name}")
            return docs
        except Exception as e:
            logger.error(f"Error getting table data: {str(e)}")
            return []
    
    def query_table(self, table_name: str, field: str, value: Any) -> List[Dict[str, Any]]:
        """Query a table for documents where field equals value.
        
        Args:
            table_name: Name of the table to query
            field: Field to query on
            value: Value to match
            
        Returns:
            List of matching documents
        """
        logger.info(f"Querying table {table_name} where {field} = {value}")
        try:
            table = self.db.table(table_name)
            User = Query()
            results = table.search(getattr(User, field) == value)
            logger.info(f"Query returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Error querying table: {str(e)}")
            return []
    
    def add_document(self, table_name: str, data: Dict[str, Any]) -> int:
        """Add a document to a specific table.
        
        Args:
            table_name: Name of the table to add to
            data: Document data to add
            
        Returns:
            ID of the inserted document
        """
        logger.info(f"Adding document to table {table_name}: {data}")
        try:
            table = self.db.table(table_name)
            doc_id = table.insert(data)
            logger.info(f"Document added with ID: {doc_id}")
            return doc_id
        except Exception as e:
            logger.error(f"Error adding document: {str(e)}")
            raise
    
    def update_document(self, table_name: str, doc_id: Union[str, int], data: Dict[str, Any]) -> bool:
        """Update a document in a specific table.
        
        Args:
            table_name: Name of the table to update
            doc_id: ID of the document to update
            data: New data for the document
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Updating document {doc_id} in table {table_name} with data: {data}")
        try:
            table = self.db.table(table_name)
            doc_id_int = int(doc_id) if isinstance(doc_id, str) and doc_id.isdigit() else doc_id
            
            # In TinyDB, we need to use the Document ID API
            # First, check if the document exists
            doc = table.get(doc_id=doc_id_int)
            if not doc:
                logger.warning(f"Document with ID {doc_id} not found in table {table_name}")
                return False
            
            # Update the document using the Document ID API
            table.update(data, doc_ids=[doc_id_int])
            logger.info(f"Document update successful")
            return True
        except Exception as e:
            logger.error(f"Error updating document: {str(e)}")
            return False
    
    def delete_document(self, table_name: str, doc_id: Union[str, int]) -> bool:
        """Delete a document from a specific table.
        
        Args:
            table_name: Name of the table to delete from
            doc_id: ID of the document to delete
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Deleting document {doc_id} from table {table_name}")
        try:
            table = self.db.table(table_name)
            doc_id_int = int(doc_id) if isinstance(doc_id, str) and doc_id.isdigit() else doc_id
            
            # First, check if the document exists
            doc = table.get(doc_id=doc_id_int)
            if not doc:
                logger.warning(f"Document with ID {doc_id} not found in table {table_name}")
                return False
            
            # Delete the document using the Document ID API
            table.remove(doc_ids=[doc_id_int])
            logger.info(f"Document deletion successful")
            return True
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            return False
    
    def store_lead(self, lead_data: Dict[str, Any]) -> int:
        """Store lead information in the leads table.
        
        Args:
            lead_data: Lead information to store
            
        Returns:
            ID of the inserted lead document
        """
        logger.info(f"Storing lead information: {lead_data}")
        try:
            # Add timestamp if not provided
            if 'timestamp' not in lead_data:
                lead_data['timestamp'] = datetime.datetime.now().isoformat()
            
            # Store in leads table
            lead_id = self.leads_table.insert(lead_data)
            logger.info(f"Lead stored with ID: {lead_id}")
            return lead_id
        except Exception as e:
            logger.error(f"Error storing lead: {str(e)}")
            raise
    
    def backup_database(self, backup_dir: str = None) -> Dict[str, Any]:
        """Create a backup of the database.
        
        Args:
            backup_dir: Directory to store the backup (defaults to same directory as database)
            
        Returns:
            Dictionary with backup result information
        """
        logger.info("Creating database backup")
        try:
            # Get the database path
            db_path = self.db_path
            
            # Generate backup filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{os.path.basename(db_path)}.backup_{timestamp}"
            
            # Determine backup directory
            if not backup_dir:
                backup_dir = os.path.dirname(db_path)
            
            # Create backup directory if it doesn't exist
            os.makedirs(backup_dir, exist_ok=True)
            
            # Full path to backup file
            backup_path = os.path.join(backup_dir, backup_filename)
            
            # Read the database file
            with open(db_path, 'r') as src_file:
                db_contents = src_file.read()
            
            # Write to backup file
            with open(backup_path, 'w') as backup_file:
                backup_file.write(db_contents)
            
            logger.info(f"Database backup created at: {backup_path}")
            return {
                "success": True,
                "backup_path": backup_path,
                "timestamp": timestamp
            }
        except Exception as e:
            error_msg = f"Error creating database backup: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            } 