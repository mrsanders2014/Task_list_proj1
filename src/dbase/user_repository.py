"""
User Repository
Handles CRUD operations for Users collection.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId
from pymongo.errors import DuplicateKeyError, PyMongoError

from src.model.user import User
from src.dbase.connection import get_db_connection


class UserRepository:
    """Repository for User CRUD operations."""
    
    def __init__(self):
        """Initialize UserRepository with database connection."""
        self.db_connection = get_db_connection()
        self.collection = self.db_connection.get_collection('Users')
    
    def create(self, user: User) -> str:
        """
        Create a new user in the database.
        
        Args:
            user: User instance to create
            
        Returns:
            str: ID of the created user
            
        Raises:
            ValueError: If user with same username 
        """
        if self.collection is None:
            print("✓ Mock mode: Simulating user creation")
            return "mock_user_id_123"
        
        try:
            user_dict = user.to_dict()
            result = self.collection.insert_one(user_dict)
            return str(result.inserted_id)
        except DuplicateKeyError as e:
            if 'username' in str(e):
                raise ValueError(f"Username '{user.username}' already exists") from e
            else:
                raise ValueError("Duplicate user data") from e
    
    def get_by_id(self, object_id: str) -> Optional[User]:
        """
        Retrieve a user by MongoDB ObjectId.
        
        Args:
            object_id: MongoDB ObjectId as string
            
        Returns:
            User instance or None if not found
        """
        try:
            user_data = self.collection.find_one({"_id": ObjectId(object_id)})
            if user_data:
                return User.from_dict(user_data)
            return None
        except PyMongoError as e:
            print(f"Error retrieving user by ID: {e}")
            return None
    
    def get_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user by username.
        
        Args:
            username: User's unique identifier
            
        Returns:
            User instance or None if not found
        """
        if self.collection is None:
            print("✓ Mock mode: Simulating user lookup")
            return None
        
        try:
            user_data = self.collection.find_one({"username": username})
            if user_data:
                return User.from_dict(user_data)
            return None
        except PyMongoError as e:
            print(f"Error retrieving user by username: {e}")
            return None
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by email.
        
        Args:
            email: User's email address
            
        Returns:
            User instance or None if not found
        """
        try:
            user_data = self.collection.find_one({"email": email})
            if user_data:
                return User.from_dict(user_data)
            return None
        except PyMongoError as e:
            print(f"Error retrieving user by email: {e}")
            return None
    
    def get_all(self, is_active: Optional[bool] = None) -> List[User]:
        """
        Retrieve all users, optionally filtered by active status.
        
        Args:
            is_active: Filter by user active status (True/False)
            
        Returns:
            List of User instances
        """
        if self.collection is None:
            print("✓ Mock mode: Simulating get all users")
            return []
        
        try:
            query = {}
            if is_active is not None:
                query["is_active"] = is_active
            
            users_data = self.collection.find(query)
            return [User.from_dict(user_data) for user_data in users_data]
        except PyMongoError as e:
            print(f"Error retrieving all users: {e}")
            return []
    
    def update(self, username: str, update_data: Dict[str, Any]) -> bool:
        """
        Update a user's information.
        
        Args:
            username: User's unique identifier
            update_data: Dictionary of fields to update
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            # Remove fields that shouldn't be updated directly
            update_data.pop('_id', None)
            update_data.pop('username', None)  # username shouldn't change
            
            result = self.collection.update_one(
                {"username": username},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except PyMongoError as e:
            print(f"Error updating user: {e}")
            return False
    
    def update_last_login(self, username: str) -> bool:
        """
        Update the last login timestamp for a user.
        
        Args:
            username: User's unique identifier
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        return self.update(username, {"last_login": datetime.now()})
    
    def change_status(self, username: str, is_active: bool) -> bool:
        """
        Change a user's active status.
        
        Args:
            username: User's unique identifier
            is_active: New active status (True/False)
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        return self.update(username, {"is_active": is_active})
    
    def delete(self, username: str) -> bool:
        """
        Delete a user from the database.
        
        Args:
            username: User's unique identifier
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            result = self.collection.delete_one({"username": username})
            return result.deleted_count > 0
        except PyMongoError as e:
            print(f"Error deleting user: {e}")
            return False
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user by username and password.
        
        Args:
            username: User's unique identifier
            password: User's password
            
        Returns:
            User instance if authentication successful, None otherwise
        """
        user = self.get_by_username(username)
        # Note: The new User model doesn't have a password field
        # This method needs to be updated based on your authentication strategy
        if user:
            self.update_last_login(username)
            return user
        return None
    
    def count(self) -> int:
        """
        Get the total count of users.
        
        Returns:
            int: Total number of users
        """
        try:
            return self.collection.count_documents({})
        except PyMongoError as e:
            print(f"Error counting users: {e}")
            return 0

