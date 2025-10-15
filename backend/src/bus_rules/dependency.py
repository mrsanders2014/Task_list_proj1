"""
Dependency injection for FastAPI application with Beanie ODM
Provides database and service instances for route handlers
"""

from backend.src.dbase.beanie_init import BeanieDatabase, get_beanie_db

async def get_database() -> BeanieDatabase:
    """
    Get Beanie database instance
    Returns:
        BeanieDatabase: Database instance
    """
    return await get_beanie_db()