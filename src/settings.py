# settings.py
import os
from dotenv import load_dotenv


def Setup():
    """
    Load and validate environment variables for the application.
    
    Returns:
        tuple: A tuple containing (MONGO_URI, DB_NAME)
        
    Raises:
        Exception: If MONGO_URI environment variable is not set
    """
    # Load environment variables from .env file
    load_dotenv()

    # Get the MongoDB connection URI
    MONGO_URI = os.getenv("project_db_url")

    # Exit if the project_db_url environment variable is not set
    if not MONGO_URI:
        raise Exception("project_db_url environment variable is not set.")

    # Get database name from environment variable or extract from URI
    DB_NAME = os.getenv('DATABASE_NAME')
    if not DB_NAME:
        # Try to extract from URI if not set in environment
        uri_parts = MONGO_URI.split('/')
        if len(uri_parts) > 3 and uri_parts[-1]:
            DB_NAME = uri_parts[-1].split('?')[0]
        else:
            DB_NAME = 'task_manager'  # Default database name
    
    return MONGO_URI, DB_NAME

