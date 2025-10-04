"""
User Model
Defines the User data structure and validation.
"""
from datetime import datetime
from typing import Optional, Dict, Any
from bson import ObjectId


class User:
    """User model representing a user in the system."""
    
    def __init__(
        self,
        firstname: str,
        lastname: str,
        userid: str,
        email: str,
        password: str,
        status: str = "active",
        last_login: Optional[datetime] = None,
        _id: Optional[ObjectId] = None
    ):
        """
        Initialize a User instance.
        
        Args:
            firstname: User's first name
            lastname: User's last name
            userid: Unique user identifier
            email: User's email address
            password: User's password (should be hashed in production)
            status: User status (active or inactive)
            last_login: Timestamp of last login
            _id: MongoDB ObjectId
        """
        self._id = _id
        self.firstname = firstname
        self.lastname = lastname
        self.userid = userid
        self.email = email
        self.password = password
        self.status = status
        self.last_login = last_login or datetime.now()
        
        self._validate()
    
    def _validate(self) -> None:
        """Validate user data."""
        if not self.firstname or not self.firstname.strip():
            raise ValueError("First name is required")
        
        if not self.lastname or not self.lastname.strip():
            raise ValueError("Last name is required")
        
        if not self.userid or not self.userid.strip():
            raise ValueError("User ID is required")
        
        if not self.email or not self.email.strip():
            raise ValueError("Email is required")
        
        if '@' not in self.email:
            raise ValueError("Invalid email format")
        
        if not self.password or len(self.password) < 6:
            raise ValueError("Password must be at least 6 characters")
        
        if self.status not in ["active", "inactive"]:
            raise ValueError("Status must be 'active' or 'inactive'")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert User instance to dictionary for MongoDB storage.
        
        Returns:
            Dict containing user data
        """
        data = {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "userid": self.userid,
            "email": self.email,
            "password": self.password,
            "status": self.status,
            "last_login": self.last_login
        }
        
        if self._id is not None:
            data["_id"] = self._id
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """
        Create User instance from dictionary.
        
        Args:
            data: Dictionary containing user data
            
        Returns:
            User instance
        """
        return cls(
            firstname=data.get('firstname', ''),
            lastname=data.get('lastname', ''),
            userid=data.get('userid', ''),
            email=data.get('email', ''),
            password=data.get('password', ''),
            status=data.get('status', 'active'),
            last_login=data.get('last_login'),
            _id=data.get('_id')
        )
    
    def __str__(self) -> str:
        """String representation of User."""
        return f"User({self.userid}: {self.firstname} {self.lastname} - {self.email})"
    
    def __repr__(self) -> str:
        """Debug representation of User."""
        return self.__str__()

