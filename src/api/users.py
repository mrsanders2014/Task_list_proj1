"""
User API endpoints for FastAPI application.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import JSONResponse

from src.model.user import User
from src.dbase.user_repository import UserRepository
from src.api.schemas import (
    UserCreateSchema, 
    UserUpdateSchema, 
    UserResponseSchema
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateSchema):
    """
    Create a new user.
    
    Args:
        user_data: User creation data
        
    Returns:
        Created user information
        
    Raises:
        HTTPException: If user creation fails
    """
    try:
        user_repo = UserRepository()
        
        # Check if username already exists
        existing_user = user_repo.get_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Username '{user_data.username}' already exists"
            )
        
        # Check if email already exists
        existing_email = user_repo.get_by_email(user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email '{user_data.email}' already exists"
            )
        
        # Create new user
        user = User(
            username=user_data.username,
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        
        user_id = user_repo.create(user)
        user._id = user_id
        
        return user.to_response()
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        ) from e


@router.get("/", response_model=List[UserResponseSchema])
async def get_users(is_active: Optional[bool] = Query(None, description="Filter by active status")):
    """
    Get all users, optionally filtered by active status.
    
    Args:
        is_active: Optional filter by user active status
        
    Returns:
        List of users
    """
    try:
        user_repo = UserRepository()
        users = user_repo.get_all(is_active=is_active)
        return [user.to_response() for user in users]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve users: {str(e)}"
        ) from e


@router.get("/{user_id}", response_model=UserResponseSchema)
async def get_user(user_id: str):
    """
    Get a user by ID.
    
    Args:
        user_id: User's MongoDB ObjectId
        
    Returns:
        User information
        
    Raises:
        HTTPException: If user not found
    """
    try:
        user_repo = UserRepository()
        user = user_repo.get_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID '{user_id}' not found"
            )
        
        return user.to_response()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user: {str(e)}"
        ) from e


@router.get("/username/{username}", response_model=UserResponseSchema)
async def get_user_by_username(username: str):
    """
    Get a user by username.
    
    Args:
        username: User's username
        
    Returns:
        User information
        
    Raises:
        HTTPException: If user not found
    """
    try:
        user_repo = UserRepository()
        user = user_repo.get_by_username(username)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with username '{username}' not found"
            )
        
        return user.to_response()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user: {str(e)}"
        ) from e


@router.put("/{user_id}", response_model=UserResponseSchema)
async def update_user(user_id: str, user_data: UserUpdateSchema):
    """
    Update a user's information.
    
    Args:
        user_id: User's MongoDB ObjectId
        user_data: User update data
        
    Returns:
        Updated user information
        
    Raises:
        HTTPException: If user not found or update fails
    """
    try:
        user_repo = UserRepository()
        
        # Check if user exists
        user = user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID '{user_id}' not found"
            )
        
        # Prepare update data
        update_data = {}
        if user_data.email is not None:
            # Check if email is already taken by another user
            existing_email = user_repo.get_by_email(user_data.email)
            if existing_email and existing_email.username != user.username:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Email '{user_data.email}' already exists"
                )
            update_data["email"] = user_data.email
        
        if user_data.first_name is not None:
            update_data["first_name"] = user_data.first_name
        
        if user_data.last_name is not None:
            update_data["last_name"] = user_data.last_name
        
        if user_data.is_active is not None:
            update_data["is_active"] = user_data.is_active
        
        # Update user
        if update_data:
            success = user_repo.update(user.username, update_data)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update user"
                )
        
        # Return updated user
        updated_user = user_repo.get_by_id(user_id)
        return updated_user.to_response()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}"
        ) from e


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    """
    Delete a user.
    
    Args:
        user_id: User's MongoDB ObjectId
        
    Raises:
        HTTPException: If user not found or deletion fails
    """
    try:
        user_repo = UserRepository()
        
        # Check if user exists
        user = user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID '{user_id}' not found"
            )
        
        # Delete user
        success = user_repo.delete(user.username)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete user"
            )
        
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {str(e)}"
        ) from e


@router.patch("/{user_id}/status", response_model=UserResponseSchema)
async def change_user_status(user_id: str, is_active: bool):
    """
    Change a user's active status.
    
    Args:
        user_id: User's MongoDB ObjectId
        is_active: New active status
        
    Returns:
        Updated user information
        
    Raises:
        HTTPException: If user not found or update fails
    """
    try:
        user_repo = UserRepository()
        
        # Check if user exists
        user = user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID '{user_id}' not found"
            )
        
        # Update status
        success = user_repo.change_status(user.username, is_active)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to change user status"
            )
        
        # Return updated user
        updated_user = user_repo.get_by_id(user_id)
        return updated_user.to_response()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change user status: {str(e)}"
        ) from e
