"""
MongoDB Database Connection Module
Handles connection to MongoDB using environment variables.
"""
import os
from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure, ConfigurationError
from dotenv import load_dotenv


class DatabaseConnection:
    """Manages MongoDB database connection."""
    
    _instance: Optional['DatabaseConnection'] = None
    _client: Optional[MongoClient] = None
    _database: Optional[Database] = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one database connection."""
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize database connection."""
        if self._client is None:
            load_dotenv()
            self._connect()
    
    def _connect(self) -> None:
        """Establish connection to MongoDB."""
        try:
#            # Get MongoDB URL from environment variable
            mongo_url = os.getenv('project_db_url')
            database_name = os.getenv('DATABASE_NAME', 'task_manager')
            
            # Check if we're in mock mode
            if os.getenv('MOCK_MODE', 'false').lower() == 'true':
                print(f"✓ Running in MOCK mode - no actual MongoDB connection")
                self._client = None
                self._database = None
                return
            
            # Create MongoDB client
            self._client = MongoClient(
                mongo_url,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000
            )
            
            # Test the connection
            self._client.admin.command('ping')
            
            # Get database reference
            self._database = self._client[database_name]
            
            print(f"✓ Successfully connected to MongoDB database: {database_name}")
            
        except ConnectionFailure as e:
            print(f"✗ Failed to connect to MongoDB: {e}")
            print("💡 Tip: Start MongoDB service or set MOCK_MODE=true for testing")
            raise
        except ConfigurationError as e:
            print(f"✗ MongoDB configuration error: {e}")
            print("💡 Tip: Check your MongoDB connection string or set MOCK_MODE=true for testing")
            raise
        except Exception as e:
            print(f"✗ Unexpected error connecting to MongoDB: {e}")
            print("💡 Tip: Set MOCK_MODE=true for testing without MongoDB")
            raise
    
    def get_database(self) -> Database:
        """
        Get the database instance.
        
        Returns:
            Database: MongoDB database instance
        """
        if self._database is None and os.getenv('MOCK_MODE', 'false').lower() != 'true':
            self._connect()
        return self._database
    
    def get_collection(self, collection_name: str):
        """
        Get a specific collection from the database.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Collection: MongoDB collection instance or None in mock mode
        """
        if os.getenv('MOCK_MODE', 'false').lower() == 'true':
            print(f"✓ Mock mode: Returning None for collection '{collection_name}'")
            return None
        
        db = self.get_database()
        return db[collection_name]
    
    def close(self) -> None:
        """Close the database connection."""
        if self._client is not None:
            self._client.close()
            self._client = None
            self._database = None
            print("✓ Database connection closed")
    
    def create_indexes(self) -> None:
        """Create necessary indexes for collections."""
        if os.getenv('MOCK_MODE', 'false').lower() == 'true':
            print("✓ Mock mode: Skipping index creation")
            return
        
        try:
            db = self.get_database()
            
            # Users collection indexes
            users_collection = db['Users']
            users_collection.create_index('username', unique=True)
            users_collection.create_index('email', unique=True)
            
            # Tasks collection indexes
            tasks_collection = db['Tasks']
            tasks_collection.create_index('user_id')
            tasks_collection.create_index('status')
            tasks_collection.create_index('priority')
            tasks_collection.create_index('due_date')
            
            print("✓ Database indexes created successfully")
            
        except Exception as e:
            print(f"✗ Error creating indexes: {e}")
            raise


def get_db_connection() -> DatabaseConnection:
    """
    Get database connection instance.
    
    Returns:
        DatabaseConnection: Singleton database connection instance
    """
    return DatabaseConnection()

