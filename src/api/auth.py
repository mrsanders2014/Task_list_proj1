"""
Authentication API endpoints for JWT token management.
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.models.beanie_user import BeanieUser
from src.api.schemas import (
    UserLoginSchema,
    UserRegisterSchema,
    Token,
    UserResponseSchema
)
from src.bus_rules.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_user,
    TokenData
)

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegisterSchema):
    """
    Register a new user.

    Args:
        user_data: User registration data

    Returns:
        Created user information

    Raises:
        HTTPException: If user with given username or email already exists
    """
    # Check if username already exists
    existing_user = await BeanieUser.find_one(BeanieUser.username == user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username already exists"
        )

    # Check if email already exists
    existing_email = await BeanieUser.find_one(BeanieUser.email == user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
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
    
    await user.insert()
    return user.to_response()


@router.post("/login", response_model=Token)
async def login_user(user_credentials: UserLoginSchema):
    """
    Authenticate user and return JWT token.

    Args:
        user_credentials: User login credentials

    Returns:
        JWT access token

    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by username or email
    user = await BeanieUser.find_one(
        (BeanieUser.username == user_credentials.username) | 
        (BeanieUser.email == user_credentials.username)
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Authenticate user
    authenticated_user = authenticate_user(
        user_credentials.username,
        user_credentials.password,
        user
    )
    
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "user_id": str(user.id),
            "type": "access",
            "version": 1
        },
        expires_delta=access_token_expires
    )

    # Update last login
    user.last_login = datetime.now()
    await user.save()

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/login-form", response_model=Token)
async def login_form(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate user using OAuth2 password form (for Swagger UI).

    Args:
        form_data: OAuth2 password form data

    Returns:
        JWT access token

    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by username or email
    user = await BeanieUser.find_one(
        (BeanieUser.username == form_data.username) | 
        (BeanieUser.email == form_data.username)
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Authenticate user
    authenticated_user = authenticate_user(
        form_data.username,
        form_data.password,
        user
    )
    
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "user_id": str(user.id),
            "type": "access",
            "version": 1
        },
        expires_delta=access_token_expires
    )

    # Update last login
    user.last_login = datetime.now()
    await user.save()

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponseSchema)
async def get_current_user_info(current_user: TokenData = Depends(get_current_user)):
    """
    Get current authenticated user information.

    Args:
        current_user: Current authenticated user from JWT token

    Returns:
        Current user information
    """
    # Find user by username from token
    user = await BeanieUser.find_one(BeanieUser.username == current_user.username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user.to_response()


@router.post("/refresh", response_model=Token)
async def refresh_token(current_user: TokenData = Depends(get_current_user)):
    """
    Refresh JWT access token.

    Args:
        current_user: Current authenticated user from JWT token

    Returns:
        New JWT access token
    """
    # Create new access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={
            "sub": current_user.username,
            "user_id": current_user.user_id,
            "type": "access",
            "version": 1
        },
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
