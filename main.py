"""
Task Manager FastAPI Application
Main entry point for the FastAPI application.
"""
import uvicorn
from src.api.main import app
from src.settings import Setup


def main():
    """Main entry point for the FastAPI application."""
    try:
        MONGO_URI, DB_NAME = Setup()
        print(f"✓ MongoDB URI: {MONGO_URI}")
        print(f"✓ Database Name: {DB_NAME}")
        print("✓ Launching Task Manager FastAPI application...")
        print("✓ API Documentation available at: http://localhost:8000/docs")
        print("✓ Alternative docs at: http://localhost:8000/redoc")
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        print(f"✗ Failed to start application: {e}")
        raise


if __name__ == "__main__":
    main()
