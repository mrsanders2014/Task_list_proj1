"""
Beanie User Document Model
Defines the User document structure using Beanie ODM.
"""
from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import Field, EmailStr, validator
from pymongo import IndexModel


class BeanieUser(Document):
    """User document model using Beanie ODM."""
    
    # Required fields
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., description="User's email address")
    
    # Optional fields
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(None)
    last_login: Optional[datetime] = Field(None)
    
    # Status
    is_active: bool = Field(default=True)
    
    class Settings:
        name = "users"  # Collection name
        indexes = [
            IndexModel([("username", 1)], unique=True),
            IndexModel([("email", 1)], unique=True),
            IndexModel([("is_active", 1)]),
            IndexModel([("created_at", -1)]),
        ]
    
    @validator('username')
    @classmethod
    def validate_username(cls, v):
        """Validate username format."""
        if not v or not v.strip():
            raise ValueError('Username cannot be empty')
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        return v.strip()
    
    @validator('first_name', 'last_name')
    @classmethod
    def validate_names(cls, v):
        """Validate name fields."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    def get_full_name(self) -> str:
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return self.username
    
    def update_last_login(self) -> None:
        """Update the last login timestamp."""
        self.last_login = datetime.now()
        self.updated_at = datetime.now()
    
    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False
        self.updated_at = datetime.now()
    
    def activate(self) -> None:
        """Activate the user account."""
        self.is_active = True
        self.updated_at = datetime.now()
    
    def to_response(self) -> dict:
        """Convert user to API response format."""
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.get_full_name(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "last_login": self.last_login,
            "is_active": self.is_active
        }
    
    def __str__(self) -> str:
        """String representation of the user."""
        full_name = self.get_full_name()
        if full_name != self.username:
            return f"{self.username} ({full_name})"
        return self.username
    
    def __repr__(self) -> str:
        """Debug representation of the user."""
        return (f"BeanieUser(username='{self.username}', email='{self.email}', "
                f"first_name='{self.first_name}', last_name='{self.last_name}', "
                f"is_active={self.is_active})")
