"""
Tests for JWT authentication functionality.
"""
import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient

from main import app
from src.bus_rules.auth import create_access_token, verify_token, get_password_hash
from src.api.schemas import TokenData

client = TestClient(app)


def test_create_access_token():
    """Test JWT token creation."""
    data = {"sub": "testuser", "user_id": "123", "type": "access", "version": 1}
    token = create_access_token(data)
    assert isinstance(token, str)
    assert len(token) > 0


def test_verify_token():
    """Test JWT token verification."""
    data = {"sub": "testuser", "user_id": "123", "type": "access", "version": 1}
    token = create_access_token(data)
    
    token_data = verify_token(token)
    assert isinstance(token_data, TokenData)
    assert token_data.username == "testuser"
    assert token_data.user_id == "123"


def test_password_hashing():
    """Test password hashing functionality."""
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    assert isinstance(hashed, str)
    assert len(hashed) > 0
    assert hashed != password


def test_register_user():
    """Test user registration endpoint."""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    
    user_response = response.json()
    assert user_response["username"] == "testuser"
    assert user_response["email"] == "test@example.com"
    assert "password" not in user_response  # Password should not be returned


def test_login_user():
    """Test user login endpoint."""
    # First register a user
    user_data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    client.post("/auth/register", json=user_data)
    
    # Then login
    login_data = {
        "username": "testuser2",
        "password": "testpassword123"
    }
    
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    
    token_response = response.json()
    assert "access_token" in token_response
    assert token_response["token_type"] == "bearer"


def test_protected_endpoint_without_token():
    """Test that protected endpoints require authentication."""
    response = client.get("/users/")
    assert response.status_code == 401


def test_protected_endpoint_with_token():
    """Test that protected endpoints work with valid token."""
    # Register and login
    user_data = {
        "username": "testuser3",
        "email": "test3@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    client.post("/auth/register", json=user_data)
    
    login_data = {
        "username": "testuser3",
        "password": "testpassword123"
    }
    
    login_response = client.post("/auth/login", json=login_data)
    token = login_response.json()["access_token"]
    
    # Use token to access protected endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200


def test_get_current_user():
    """Test getting current user information."""
    # Register and login
    user_data = {
        "username": "testuser4",
        "email": "test4@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    client.post("/auth/register", json=user_data)
    
    login_data = {
        "username": "testuser4",
        "password": "testpassword123"
    }
    
    login_response = client.post("/auth/login", json=login_data)
    token = login_response.json()["access_token"]
    
    # Get current user info
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    
    user_info = response.json()
    assert user_info["username"] == "testuser4"
    assert user_info["email"] == "test4@example.com"
