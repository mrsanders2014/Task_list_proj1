"""
Unit tests for User model.
"""
import pytest
from datetime import datetime
from src.model.user import User


def test_user_creation():
    """Test creating a valid user."""
    user = User(
        username="johndoe",
        email="john@example.com",
        first_name="John",
        last_name="Doe"
    )
    
    assert user.username == "johndoe"
    assert user.email == "john@example.com"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.is_active is True
    assert isinstance(user.created_at, datetime)
    assert user.updated_at is None
    assert user.last_login is None
    assert user._id is None


def test_user_creation_with_optional_fields():
    """Test creating a user with optional fields."""
    user = User(
        username="janesmith",
        email="jane@example.com",
        first_name="Jane",
        last_name="Smith",
        is_active=False
    )
    
    assert user.username == "janesmith"
    assert user.email == "jane@example.com"
    assert user.first_name == "Jane"
    assert user.last_name == "Smith"
    assert user.is_active is False


def test_user_creation_minimal():
    """Test creating a user with only required fields."""
    user = User(
        username="minimaluser",
        email="minimal@example.com"
    )
    
    assert user.username == "minimaluser"
    assert user.email == "minimal@example.com"
    assert user.first_name is None
    assert user.last_name is None
    assert user.is_active is True


def test_user_to_dict():
    """Test converting user to dictionary."""
    user = User(
        username="johndoe",
        email="john@example.com",
        first_name="John",
        last_name="Doe"
    )
    
    user_dict = user.to_dict()
    
    assert user_dict["username"] == "johndoe"
    assert user_dict["email"] == "john@example.com"
    assert user_dict["first_name"] == "John"
    assert user_dict["last_name"] == "Doe"
    assert user_dict["is_active"] is True
    assert "created_at" in user_dict
    assert "updated_at" not in user_dict
    assert "last_login" not in user_dict
    assert "_id" not in user_dict


def test_user_to_dict_with_optional_fields():
    """Test converting user to dictionary with optional fields."""
    user = User(
        username="johndoe",
        email="john@example.com",
        first_name="John",
        last_name="Doe"
    )
    user.updated_at = datetime.now()
    user.last_login = datetime.now()
    
    user_dict = user.to_dict()
    
    assert "updated_at" in user_dict
    assert "last_login" in user_dict


def test_user_from_dict():
    """Test creating user from dictionary."""
    user_data = {
        "username": "janesmith",
        "email": "jane@example.com",
        "first_name": "Jane",
        "last_name": "Smith",
        "is_active": True,
        "created_at": datetime.now()
    }
    
    user = User.from_dict(user_data)
    
    assert user.username == "janesmith"
    assert user.email == "jane@example.com"
    assert user.first_name == "Jane"
    assert user.last_name == "Smith"
    assert user.is_active is True
    assert isinstance(user.created_at, datetime)


def test_user_from_dict_minimal():
    """Test creating user from minimal dictionary."""
    user_data = {
        "username": "minimaluser",
        "email": "minimal@example.com"
    }
    
    user = User.from_dict(user_data)
    
    assert user.username == "minimaluser"
    assert user.email == "minimal@example.com"
    assert user.first_name is None
    assert user.last_name is None
    assert user.is_active is True


def test_user_update():
    """Test updating user fields."""
    user = User(
        username="johndoe",
        email="john@example.com",
        first_name="John",
        last_name="Doe"
    )
    
    original_updated_at = user.updated_at
    
    user.update(first_name="Johnny", last_name="Doe-Smith")
    
    assert user.first_name == "Johnny"
    assert user.last_name == "Doe-Smith"
    assert user.updated_at is not None
    assert user.updated_at != original_updated_at


def test_user_get_full_name():
    """Test getting user's full name."""
    user = User(
        username="johndoe",
        email="john@example.com",
        first_name="John",
        last_name="Doe"
    )
    
    assert user.get_full_name() == "John Doe"


def test_user_get_full_name_first_only():
    """Test getting user's full name with only first name."""
    user = User(
        username="johndoe",
        email="john@example.com",
        first_name="John"
    )
    
    assert user.get_full_name() == "John"


def test_user_get_full_name_last_only():
    """Test getting user's full name with only last name."""
    user = User(
        username="johndoe",
        email="john@example.com",
        last_name="Doe"
    )
    
    assert user.get_full_name() == "Doe"


def test_user_get_full_name_no_names():
    """Test getting user's full name with no first/last names."""
    user = User(
        username="johndoe",
        email="john@example.com"
    )
    
    assert user.get_full_name() == "johndoe"


def test_user_update_last_login():
    """Test updating last login timestamp."""
    user = User(
        username="johndoe",
        email="john@example.com"
    )
    
    original_last_login = user.last_login
    
    user.update_last_login()
    
    assert user.last_login is not None
    assert user.last_login != original_last_login


def test_user_deactivate():
    """Test deactivating user account."""
    user = User(
        username="johndoe",
        email="john@example.com"
    )
    
    original_updated_at = user.updated_at
    
    user.deactivate()
    
    assert user.is_active is False
    assert user.updated_at is not None
    assert user.updated_at != original_updated_at


def test_user_activate():
    """Test activating user account."""
    user = User(
        username="johndoe",
        email="john@example.com",
        is_active=False
    )
    
    original_updated_at = user.updated_at
    
    user.activate()
    
    assert user.is_active is True
    assert user.updated_at is not None
    assert user.updated_at != original_updated_at


def test_user_str_representation():
    """Test string representation of user."""
    user = User(
        username="johndoe",
        email="john@example.com",
        first_name="John",
        last_name="Doe"
    )
    
    user_str = str(user)
    assert "johndoe" in user_str
    assert "John Doe" in user_str


def test_user_str_representation_no_names():
    """Test string representation of user with no first/last names."""
    user = User(
        username="johndoe",
        email="john@example.com"
    )
    
    user_str = str(user)
    assert user_str == "johndoe"


def test_user_repr_representation():
    """Test detailed representation of user."""
    user = User(
        username="johndoe",
        email="john@example.com",
        first_name="John",
        last_name="Doe"
    )
    
    user_repr = repr(user)
    assert "User(" in user_repr
    assert "username='johndoe'" in user_repr
    assert "email='john@example.com'" in user_repr
    assert "first_name='John'" in user_repr
    assert "last_name='Doe'" in user_repr
    assert "is_active=True" in user_repr


def test_user_to_response():
    """Test converting user to API response format."""
    user = User(
        username="johndoe",
        email="john@example.com",
        first_name="John",
        last_name="Doe"
    )
    
    response = user.to_response()
    
    assert response["username"] == "johndoe"
    assert response["email"] == "john@example.com"
    assert response["first_name"] == "John"
    assert response["last_name"] == "Doe"
    assert response["full_name"] == "John Doe"
    assert response["is_active"] is True
    assert "id" in response
    assert "created_at" in response
    assert "updated_at" in response
    assert "last_login" in response