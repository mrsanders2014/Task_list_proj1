"""
Unit tests for Beanie User model.
"""
from datetime import datetime

import pytest

from src.models.beanie_user import BeanieUser


def test_beanie_user_creation():
    """Test creating a valid BeanieUser."""
    user = BeanieUser(
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User"
    )
    
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.first_name == "Test"
    assert user.last_name == "User"
    assert user.is_active is True
    assert isinstance(user.created_at, datetime)
    assert user.updated_at is None
    assert user.last_login is None


def test_beanie_user_validation_missing_username():
    """Test user validation fails with missing username."""
    with pytest.raises(ValueError, match="Username cannot be empty"):
        BeanieUser(
            username="",
            email="test@example.com"
        )


def test_beanie_user_validation_invalid_username():
    """Test user validation fails with invalid username."""
    with pytest.raises(ValueError, match="Username can only contain letters, numbers, underscores, and hyphens"):
        BeanieUser(
            username="test@user!",
            email="test@example.com"
        )


def test_beanie_user_validation_invalid_email():
    """Test user validation fails with invalid email."""
    with pytest.raises(ValueError):
        BeanieUser(
            username="testuser",
            email="invalid-email"
        )


def test_beanie_user_get_full_name():
    """Test getting user's full name."""
    user = BeanieUser(
        username="testuser",
        email="test@example.com",
        first_name="John",
        last_name="Doe"
    )
    
    assert user.get_full_name() == "John Doe"
    
    # Test with only first name
    user.last_name = None
    assert user.get_full_name() == "John"
    
    # Test with only last name
    user.first_name = None
    user.last_name = "Doe"
    assert user.get_full_name() == "Doe"
    
    # Test with no names
    user.last_name = None
    assert user.get_full_name() == "testuser"


def test_beanie_user_activate_deactivate():
    """Test user activation and deactivation."""
    user = BeanieUser(
        username="testuser",
        email="test@example.com"
    )
    
    assert user.is_active is True
    
    # Deactivate
    user.deactivate()
    assert user.is_active is False
    assert user.updated_at is not None
    
    # Activate
    user.activate()
    assert user.is_active is True
    assert user.updated_at is not None


def test_beanie_user_update_last_login():
    """Test updating last login timestamp."""
    user = BeanieUser(
        username="testuser",
        email="test@example.com"
    )
    
    initial_updated_at = user.updated_at
    user.update_last_login()
    
    assert user.last_login is not None
    assert user.updated_at is not None
    assert user.updated_at != initial_updated_at


def test_beanie_user_to_response():
    """Test converting user to response format."""
    user = BeanieUser(
        username="testuser",
        email="test@example.com",
        first_name="John",
        last_name="Doe"
    )
    
    response = user.to_response()
    
    assert "id" in response
    assert response["username"] == "testuser"
    assert response["email"] == "test@example.com"
    assert response["first_name"] == "John"
    assert response["last_name"] == "Doe"
    assert response["full_name"] == "John Doe"
    assert response["is_active"] is True
    assert "created_at" in response


def test_beanie_user_str_representation():
    """Test string representation of user."""
    user = BeanieUser(
        username="testuser",
        email="test@example.com",
        first_name="John",
        last_name="Doe"
    )
    
    user_str = str(user)
    assert "testuser" in user_str
    assert "John Doe" in user_str
    
    # Test with no names
    user.first_name = None
    user.last_name = None
    user_str = str(user)
    assert user_str == "testuser"


def test_beanie_user_repr():
    """Test debug representation of user."""
    user = BeanieUser(
        username="testuser",
        email="test@example.com",
        first_name="John",
        last_name="Doe"
    )
    
    repr_str = repr(user)
    assert "BeanieUser" in repr_str
    assert "testuser" in repr_str
    assert "test@example.com" in repr_str
