"""
Task Manager CLI Application
Main entry point for the application.
"""
from src.Task_list_proj1.cli import main as cli_main
from src.Task_list_proj1.settings import Setup

MONGO_URI, DB_NAME = Setup()


def main():
     MONGO_URI, DB_NAME = Setup()
     print(f"Mongo URI: {MONGO_URI}")
     print(f"DB Name: {DB_NAME}")
     print("Launching Task Manager CLI application...")
     
    """Launch the Task Manager CLI application."""
    cli_main()


if __name__ == "__main__":
    main()
