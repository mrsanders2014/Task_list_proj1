"""
MongoDB database connection and client management
"""

import os
from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from dotenv import load_dotenv


class MongoDBClient:
    """MongoDB client singleton for database connections"""
    
    _instance: Optional['MongoDBClient'] = None
    _client: Optional[MongoClient] = None
    _database: Optional[Database] = None
    
    def __new__(cls):
        """Ensure only one instance of the client exists"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the MongoDB client"""
        if self._client is None:
            load_dotenv()
            self._connect()
    
    def _connect(self) -> None:
        """Connect to MongoDB using environment variables"""
        try:
            mongo_url = os.getenv('project_db_url', 'mongodb://localhost:27017/')
            database_name = os.getenv('DATABASE_NAME', 'task_list_db')
            
            self._client = MongoClient(mongo_url)
            # Test the connection
            self._client.admin.command('ping')
            print(f"✓ Successfully connected to MongoDB at {mongo_url}")
            
            self._database = self._client[database_name]
            print(f"✓ Using database: {database_name}")
            
        except Exception as e:
            print(f"✗ Error connecting to MongoDB: {e}")
            raise
    
    def get_database(self) -> Database:
        """Get the database instance"""
        if self._database is None:
            raise RuntimeError("Database not initialized")
        return self._database
    
    def get_collection(self, collection_name: str) -> Collection:
        """Get a collection from the database"""
        if self._database is None:
            raise RuntimeError("Database not initialized")
        return self._database[collection_name]
    
    def close(self) -> None:
        """Close the MongoDB connection"""
        if self._client:
            self._client.close()
            print("✓ MongoDB connection closed")
            self._client = None
            self._database = None
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


def get_mongo_client() -> MongoDBClient:
    """Get the MongoDB client instance"""
    return MongoDBClient()

