"""
Firebase Handler Module

This module provides a handler for interacting with Firebase Firestore.
It includes methods for retrieving, querying, adding, updating, and deleting data.

Optimized for Python 3.11 with enhanced typing features.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Union, Literal, TypeVar, Generic, overload

import firebase_admin
from firebase_admin import credentials, firestore

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define type variables for generic types
T = TypeVar('T')
DocumentData = Dict[str, Any]
QueryOperator = Literal['<', '<=', '==', '>=', '>', 'array-contains', 'array-contains-any', 'in', 'not-in']

class FirebaseHandler:
    """Handler for Firebase Firestore operations."""
    
    def __init__(self, credentials_path: str):
        """Initialize the Firebase handler.
        
        Args:
            credentials_path: Path to the Firebase credentials JSON file.
        
        Raises:
            FileNotFoundError: If the credentials file does not exist.
            ValueError: If the credentials file is invalid.
        """
        logger.info(f"Initializing Firebase handler with credentials from {credentials_path}")
        
        if not os.path.exists(credentials_path):
            logger.error(f"Firebase credentials file not found: {credentials_path}")
            raise FileNotFoundError(f"Firebase credentials file not found: {credentials_path}")
        
        try:
            # Initialize Firebase app if not already initialized
            if not firebase_admin._apps:
                cred = credentials.Certificate(credentials_path)
                firebase_admin.initialize_app(cred)
            
            self.db = firestore.client()
            logger.info("Firebase Firestore client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {str(e)}")
            raise ValueError(f"Failed to initialize Firebase: {str(e)}")
    
    def get_document(self, collection: str, document_id: str) -> Optional[DocumentData]:
        """Get a document from a collection by ID.
        
        Args:
            collection: The collection name.
            document_id: The document ID.
            
        Returns:
            The document data as a dictionary, or None if not found.
        """
        logger.info(f"Getting document {document_id} from collection {collection}")
        try:
            doc_ref = self.db.collection(collection).document(document_id)
            doc = doc_ref.get()
            
            if doc.exists:
                logger.info(f"Document {document_id} found")
                return doc.to_dict()
            else:
                logger.info(f"Document {document_id} not found")
                return None
        except Exception as e:
            logger.error(f"Error getting document {document_id}: {str(e)}")
            return None
    
    def get_collection_data(self, collection: str) -> List[DocumentData]:
        """Get all documents from a collection.
        
        Args:
            collection: The collection name.
            
        Returns:
            A list of document data dictionaries.
        """
        logger.info(f"Getting all documents from collection {collection}")
        try:
            docs = self.db.collection(collection).stream()
            result = [doc.to_dict() for doc in docs]
            logger.info(f"Retrieved {len(result)} documents from collection {collection}")
            return result
        except Exception as e:
            logger.error(f"Error getting collection {collection}: {str(e)}")
            return []
    
    def query_collection(
        self, 
        collection: str, 
        field: str, 
        operator: QueryOperator, 
        value: Any
    ) -> List[DocumentData]:
        """Query documents in a collection.
        
        Args:
            collection: The collection name.
            field: The field to query on.
            operator: The query operator.
            value: The value to compare against.
            
        Returns:
            A list of document data dictionaries that match the query.
        """
        logger.info(f"Querying collection {collection} where {field} {operator} {value}")
        try:
            query = self.db.collection(collection).where(field, operator, value)
            docs = query.stream()
            result = [doc.to_dict() for doc in docs]
            logger.info(f"Query returned {len(result)} documents")
            return result
        except Exception as e:
            logger.error(f"Error querying collection {collection}: {str(e)}")
            return []
    
    def add_document(self, collection: str, data: DocumentData) -> Optional[str]:
        """Add a document to a collection.
        
        Args:
            collection: The collection name.
            data: The document data.
            
        Returns:
            The ID of the new document, or None if the operation failed.
        """
        logger.info(f"Adding document to collection {collection}")
        try:
            doc_ref = self.db.collection(collection).add(data)
            document_id = doc_ref[1].id
            logger.info(f"Document added with ID: {document_id}")
            return document_id
        except Exception as e:
            logger.error(f"Error adding document to collection {collection}: {str(e)}")
            return None
    
    def update_document(self, collection: str, document_id: str, data: DocumentData) -> bool:
        """Update a document in a collection.
        
        Args:
            collection: The collection name.
            document_id: The document ID.
            data: The updated document data.
            
        Returns:
            True if the update was successful, False otherwise.
        """
        logger.info(f"Updating document {document_id} in collection {collection}")
        try:
            self.db.collection(collection).document(document_id).update(data)
            logger.info(f"Document {document_id} updated successfully")
            return True
        except Exception as e:
            logger.error(f"Error updating document {document_id}: {str(e)}")
            return False
    
    def delete_document(self, collection: str, document_id: str) -> bool:
        """Delete a document from a collection.
        
        Args:
            collection: The collection name.
            document_id: The document ID.
            
        Returns:
            True if the deletion was successful, False otherwise.
        """
        logger.info(f"Deleting document {document_id} from collection {collection}")
        try:
            self.db.collection(collection).document(document_id).delete()
            logger.info(f"Document {document_id} deleted successfully")
            return True
        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {str(e)}")
            return False
    
    @overload
    def batch_operation(self, operations: List[Dict[str, Any]]) -> bool: ...
    
    def batch_operation(self, operations: List[Dict[str, Any]]) -> bool:
        """Perform a batch operation on multiple documents.
        
        Args:
            operations: A list of operation dictionaries, each containing:
                - 'type': The operation type ('add', 'update', or 'delete')
                - 'collection': The collection name
                - 'document_id': The document ID (not required for 'add')
                - 'data': The document data (not required for 'delete')
                
        Returns:
            True if all operations were successful, False otherwise.
        """
        logger.info(f"Performing batch operation with {len(operations)} operations")
        try:
            batch = self.db.batch()
            
            for op in operations:
                op_type = op.get('type')
                collection = op.get('collection')
                document_id = op.get('document_id')
                data = op.get('data', {})
                
                if not collection:
                    logger.error("Missing collection name in batch operation")
                    return False
                
                if op_type == 'add':
                    doc_ref = self.db.collection(collection).document()
                    batch.set(doc_ref, data)
                elif op_type == 'update':
                    if not document_id:
                        logger.error("Missing document_id for update operation")
                        return False
                    doc_ref = self.db.collection(collection).document(document_id)
                    batch.update(doc_ref, data)
                elif op_type == 'delete':
                    if not document_id:
                        logger.error("Missing document_id for delete operation")
                        return False
                    doc_ref = self.db.collection(collection).document(document_id)
                    batch.delete(doc_ref)
                else:
                    logger.error(f"Unknown operation type: {op_type}")
                    return False
            
            batch.commit()
            logger.info("Batch operation completed successfully")
            return True
        except Exception as e:
            logger.error(f"Error in batch operation: {str(e)}")
            return False 