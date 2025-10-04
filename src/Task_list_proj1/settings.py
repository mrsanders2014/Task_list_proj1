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
    MONGO_URI = os.getenv("MONGO_URI")

    # Exit if the MONGO_URI environment variable is not set
    if not MONGO_URI:
        raise Exception("MONGO_URI environment variable is not set.")

    # (Optional) Extract the database name from the URI
    DB_NAME = MONGO_URI.split('/')[-1].split('?')[0]
    
    return MONGO_URI, DB_NAME

