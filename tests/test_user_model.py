"""
Unit tests for User model.
"""
import pytest
from datetime import datetime
from src.Task_list_proj1.model.user import User


def test_user_creation():
    """Test creating a valid user."""
    user = User(
        firstname="John",
        lastname="Doe",
        userid="johndoe",
        email="john@example.com",
        password="password123",
        status="active"
    )
    
    assert user.firstname == "John"
    assert user.lastname == "Doe"
    assert user.userid == "johndoe"
    assert user.email == "john@example.com"
    assert user.password == "password123"
    assert user.status == "active"
    assert isinstance(user.last_login, datetime)


def test_user_validation_missing_firstname():
    """Test user validation fails with missing firstname."""
    with pytest.raises(ValueError, match="First name is required"):
        User(
            firstname="",
            lastname="Doe",
            userid="johndoe",
            email="john@example.com",
            password="password123"
        )


def test_user_validation_missing_email():
    """Test user validation fails with missing email."""
    with pytest.raises(ValueError, match="Email is required"):
        User(
            firstname="John",
            lastname="Doe",
            userid="johndoe",
            email="",
            password="password123"
        )


def test_user_validation_invalid_email():
    """Test user validation fails with invalid email format."""
    with pytest.raises(ValueError, match="Invalid email format"):
        User(
            firstname="John",
            lastname="Doe",
            userid="johndoe",
            email="invalid-email",
            password="password123"
        )


def test_user_validation_short_password():
    """Test user validation fails with short password."""
    with pytest.raises(ValueError, match="Password must be at least 6 characters"):
        User(
            firstname="John",
            lastname="Doe",
            userid="johndoe",
            email="john@example.com",
            password="12345"
        )


def test_user_validation_invalid_status():
    """Test user validation fails with invalid status."""
    with pytest.raises(ValueError, match="Status must be 'active' or 'inactive'"):
        User(
            firstname="John",
            lastname="Doe",
            userid="johndoe",
            email="john@example.com",
            password="password123",
            status="suspended"
        )


def test_user_to_dict():
    """Test converting user to dictionary."""
    user = User(
        firstname="John",
        lastname="Doe",
        userid="johndoe",
        email="john@example.com",
        password="password123"
    )
    
    user_dict = user.to_dict()
    
    assert user_dict["firstname"] == "John"
    assert user_dict["lastname"] == "Doe"
    assert user_dict["userid"] == "johndoe"
    assert user_dict["email"] == "john@example.com"
    assert user_dict["password"] == "password123"
    assert user_dict["status"] == "active"
    assert "last_login" in user_dict


def test_user_from_dict():
    """Test creating user from dictionary."""
    user_data = {
        "firstname": "Jane",
        "lastname": "Smith",
        "userid": "janesmith",
        "email": "jane@example.com",
        "password": "securepass",
        "status": "active"
    }
    
    user = User.from_dict(user_data)
    
    assert user.firstname == "Jane"
    assert user.lastname == "Smith"
    assert user.userid == "janesmith"
    assert user.email == "jane@example.com"
    assert user.password == "securepass"
    assert user.status == "active"


def test_user_str_representation():
    """Test string representation of user."""
    user = User(
        firstname="John",
        lastname="Doe",
        userid="johndoe",
        email="john@example.com",
        password="password123"
    )
    
    user_str = str(user)
    assert "johndoe" in user_str
    assert "John" in user_str
    assert "Doe" in user_str
    assert "john@example.com" in user_str

