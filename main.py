"""
Task Manager CLI Application
Main entry point for the application.
"""
from src.User_int.cli import main as cli_main
from src.settings import Setup


def main():
    MONGO_URI, DB_NAME = Setup()
    print(f"Mongo URI: {MONGO_URI}")
    print(f"DB Name: {DB_NAME}")
    print("Launching Task Manager CLI application...")
    cli_main()


if __name__ == "__main__":
    main()
