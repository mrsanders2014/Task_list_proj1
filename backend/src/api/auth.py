"""
Authentication API endpoints for JWT token management.
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm

from backend.src.models.beanie_user import BeanieUser
from backend.src.api.schemas import (
    UserLoginSchema,
    UserRegisterSchema,
    Token,
    UserResponseSchema
)
from backend.src.bus_rules.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_user,
    set_auth_cookie,
    clear_auth_cookie,
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


@router.post("/login", response_model=UserResponseSchema)
async def login_user(user_credentials: UserLoginSchema, response: Response):
    """
    Authenticate user and set JWT token as HTTP-only cookie.

    Args:
        user_credentials: User login credentials
        response: FastAPI response object

    Returns:
        User information

    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by username or email
    user = await BeanieUser.find_one(BeanieUser.username == user_credentials.username)
    if not user:
        user = await BeanieUser.find_one(BeanieUser.email == user_credentials.username)
    
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

    # Set token as HTTP-only cookie
    set_auth_cookie(response, access_token, access_token_expires)

    # Update last login
    user.last_login = datetime.now()
    await user.save()

    return user.to_response()


@router.post("/login-form", response_model=Token)
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(), response: Response = None):
    """
    Authenticate user using OAuth2 password form (for Swagger UI).
    Returns token in response body for API documentation compatibility.

    Args:
        form_data: OAuth2 password form data
        response: FastAPI response object

    Returns:
        JWT access token

    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by username or email
    user = await BeanieUser.find_one(BeanieUser.username == form_data.username)
    if not user:
        user = await BeanieUser.find_one(BeanieUser.email == form_data.username)
    
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

    # Set token as HTTP-only cookie if response is available
    if response:
        set_auth_cookie(response, access_token, access_token_expires)

    # Update last login
    user.last_login = datetime.now()
    await user.save()

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponseSchema)
async def get_current_user_info(request: Request):
    """
    Get current authenticated user information.

    Args:
        request: FastAPI request object

    Returns:
        Current user information
    """
    from backend.src.bus_rules.auth import verify_token
    
    # Try to get token from Authorization header first
    authorization = request.headers.get("Authorization")
    token = None
    
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
    else:
        # Fall back to cookie
        token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # Verify the token
        token_data = verify_token(token)
        
        # Find user by username from token
        user = await BeanieUser.find_one(BeanieUser.username == token_data.username)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user.to_response()
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


@router.post("/refresh", response_model=UserResponseSchema)
async def refresh_token(current_user: TokenData = Depends(get_current_user), response: Response = None):
    """
    Refresh JWT access token.

    Args:
        current_user: Current authenticated user from JWT token
        response: FastAPI response object

    Returns:
        User information with new token set as cookie
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

    # Set new token as HTTP-only cookie
    if response:
        set_auth_cookie(response, access_token, access_token_expires)

    # Get user information
    user = await BeanieUser.find_one(BeanieUser.username == current_user.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user.to_response()


@router.post("/logout")
async def logout_user(response: Response):
    """
    Logout user by clearing the authentication cookie.

    Args:
        response: FastAPI response object

    Returns:
        Success message
    """
    clear_auth_cookie(response)
    return {"message": "Successfully logged out"}
