"""
Beanie Database Initialization Module
Handles Beanie ODM initialization and database connection.
"""
import os
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv

from src.models import BeanieUser, BeanieTask


class BeanieDatabase:
    """Manages Beanie ODM database connection and initialization."""
    
    _instance: Optional['BeanieDatabase'] = None
    _client: Optional[AsyncIOMotorClient] = None
    _initialized: bool = False
    
    def __new__(cls):
        """Singleton pattern to ensure only one database connection."""
        if cls._instance is None:
            cls._instance = super(BeanieDatabase, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize Beanie database connection."""
        if not self._initialized:
            load_dotenv()
            self._initialized = True
    
    async def initialize(self) -> None:
        """Initialize Beanie with MongoDB connection."""
        try:
            # Get MongoDB URL from environment variable
            mongo_url = os.getenv('project_db_url')
            database_name = os.getenv('DATABASE_NAME', 'task_manager')
            
            # Check if we're in mock mode
            if os.getenv('MOCK_MODE', 'false').lower() == 'true':
                print("✓ Running in MOCK mode - no actual MongoDB connection")
                self._client = None
                return
            
            if not mongo_url:
                raise ValueError("project_db_url environment variable is not set")
            
            # Create async MongoDB client
            self._client = AsyncIOMotorClient(
                mongo_url,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000
            )
            
            # Test the connection
            await self._client.admin.command('ping')
            
            # Get database reference
            database = self._client[database_name]
            
            # Initialize Beanie with document models
            await init_beanie(
                database=database,  # type: ignore[arg-type]
                document_models=[
                    BeanieUser,
                    BeanieTask
                ]
            )
            
            print(f"✓ Successfully initialized Beanie with MongoDB database: {database_name}")
            print("✓ Document models registered: User, Task")
            
        except (ConnectionError, OSError, ValueError) as e:
            print(f"✗ Failed to initialize Beanie: {e}")
            print("💡 Tip: Check your MongoDB connection string or set MOCK_MODE=true for testing")
            raise
    
    async def close(self) -> None:
        """Close the database connection."""
        if self._client is not None:
            self._client.close()
            self._client = None
            print("✓ Beanie database connection closed")
    
    def is_connected(self) -> bool:
        """Check if database is connected."""
        return self._client is not None and not os.getenv('MOCK_MODE', 'false').lower() == 'true'
    
    async def health_check(self) -> bool:
        """Perform a health check on the database connection."""
        if not self.is_connected():
            return False
        
        try:
            if self._client:
                await self._client.admin.command('ping')
                return True
            return False
        except (ConnectionError, OSError):
            return False


class BeanieManager:
    """Manages the global Beanie database instance."""
    
    _instance: Optional[BeanieDatabase] = None
    
    @classmethod
    async def get_db(cls) -> BeanieDatabase:
        """
        Get Beanie database instance.
        
        Returns:
            BeanieDatabase: Singleton Beanie database instance
        """
        if cls._instance is None:
            cls._instance = BeanieDatabase()
            await cls._instance.initialize()
        return cls._instance
    
    @classmethod
    async def initialize(cls) -> None:
        """
        Initialize Beanie database connection.
        This function should be called during application startup.
        """
        await cls.get_db()
    
    @classmethod
    async def close(cls) -> None:
        """
        Close Beanie database connection.
        This function should be called during application shutdown.
        """
        if cls._instance is not None:
            await cls._instance.close()
            cls._instance = None


# Convenience functions for backward compatibility
async def get_beanie_db() -> BeanieDatabase:
    """Get Beanie database instance."""
    return await BeanieManager.get_db()


async def initialize_beanie() -> None:
    """Initialize Beanie database connection."""
    await BeanieManager.initialize()


async def close_beanie() -> None:
    """Close Beanie database connection."""
    await BeanieManager.close()
