"""
Beanie User API endpoints for FastAPI application.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Query, Depends

from src.models.beanie_user import BeanieUser
from src.api.schemas import (
    UserCreateSchema, 
    UserUpdateSchema, 
    UserResponseSchema
)
from src.bus_rules.auth import get_password_hash, get_current_user, TokenData

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
        HTTPException: If user creation fails or username/email already exists
    """
    try:
        # Check if username already exists
        existing_user = await BeanieUser.find_one(BeanieUser.username == user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Username '{user_data.username}' already exists"
            )
        
        # Check if email already exists
        existing_email = await BeanieUser.find_one(BeanieUser.email == user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email '{user_data.email}' already exists"
            )
        
        # Hash the password
        hashed_password = get_password_hash(user_data.password)
        
        # Create new user
        user = BeanieUser(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        
        # Save to database
        await user.insert()
        
        return user.to_response()
        
    except HTTPException:
        raise
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
async def get_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of users to return"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    _current_user: TokenData = Depends(get_current_user)
):
    """
    Retrieve all users with optional filtering and pagination.
    
    Args:
        skip: Number of users to skip
        limit: Maximum number of users to return
        is_active: Filter by active status
        
    Returns:
        List of users
        
    Raises:
        HTTPException: If retrieval fails
    """
    try:
        # Build query
        query = {}
        if is_active is not None:
            query["is_active"] = is_active
        
        # Find users with pagination
        users = await BeanieUser.find(query).skip(skip).limit(limit).to_list()
        
        return [user.to_response() for user in users]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve users: {str(e)}"
        ) from e


@router.get("/{user_id}", response_model=UserResponseSchema)
async def get_user(user_id: str, current_user: TokenData = Depends(get_current_user)):
    """
    Retrieve a specific user by ID.
    
    Args:
        user_id: User ID
        
    Returns:
        User information
        
    Raises:
        HTTPException: If user not found or retrieval fails
    """
    try:
        user = await BeanieUser.get(user_id)
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


@router.put("/{user_id}", response_model=UserResponseSchema)
async def update_user(user_id: str, user_data: UserUpdateSchema, current_user: TokenData = Depends(get_current_user)):
    """
    Update an existing user.
    
    Args:
        user_id: User ID
        user_data: User update data
        
    Returns:
        Updated user information
        
    Raises:
        HTTPException: If user not found, update fails, or email already exists
    """
    try:
        # Find existing user
        user = await BeanieUser.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID '{user_id}' not found"
            )
        
        # Check if email is being updated and if it's already taken
        if user_data.email is not None and user_data.email != user.email:
            existing_email = await BeanieUser.find_one(BeanieUser.email == user_data.email)
            if existing_email and existing_email.id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Email '{user_data.email}' already exists"
                )
        
        # Update user fields
        update_data = {}
        if user_data.username is not None:
            update_data["username"] = user_data.username
        if user_data.email is not None:
            update_data["email"] = user_data.email
        if user_data.first_name is not None:
            update_data["first_name"] = user_data.first_name
        if user_data.last_name is not None:
            update_data["last_name"] = user_data.last_name
        
        # Apply updates
        for field, value in update_data.items():
            setattr(user, field, value)
        
        # Update timestamp
        user.updated_at = user.updated_at or user.created_at
        
        # Save changes
        await user.save()
        
        return user.to_response()
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}"
        ) from e


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, current_user: TokenData = Depends(get_current_user)):
    """
    Delete a user.
    
    Args:
        user_id: User ID
        
    Raises:
        HTTPException: If user not found or deletion fails
    """
    try:
        user = await BeanieUser.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID '{user_id}' not found"
            )
        
        await user.delete()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {str(e)}"
        ) from e


@router.patch("/{user_id}/status", response_model=UserResponseSchema)
async def change_user_status(user_id: str, is_active: bool, current_user: TokenData = Depends(get_current_user)):
    """
    Change user active status.
    
    Args:
        user_id: User ID
        is_active: New active status
        
    Returns:
        Updated user information
        
    Raises:
        HTTPException: If user not found or status change fails
    """
    try:
        user = await BeanieUser.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID '{user_id}' not found"
            )
        
        # Update status
        if is_active:
            user.activate()
        else:
            user.deactivate()
        
        # Save changes
        await user.save()
        
        return user.to_response()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change user status: {str(e)}"
        ) from e


@router.get("/username/{username}", response_model=UserResponseSchema)
async def get_user_by_username(username: str):
    """
    Retrieve a user by username.
    
    Args:
        username: Username
        
    Returns:
        User information
        
    Raises:
        HTTPException: If user not found or retrieval fails
    """
    try:
        user = await BeanieUser.find_one(BeanieUser.username == username)
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


@router.get("/email/{email}", response_model=UserResponseSchema)
async def get_user_by_email(email: str):
    """
    Retrieve a user by email.
    
    Args:
        email: Email address
        
    Returns:
        User information
        
    Raises:
        HTTPException: If user not found or retrieval fails
    """
    try:
        user = await BeanieUser.find_one(BeanieUser.email == email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email '{email}' not found"
            )
        
        return user.to_response()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user: {str(e)}"
        ) from e
