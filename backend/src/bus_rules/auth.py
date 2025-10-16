"""
Authentication utilities for JWT token handling
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from dotenv import load_dotenv

from backend.src.api.schemas import TokenData

# Load environment variables
load_dotenv()

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secure-secret-key-here-32-chars-min")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
COOKIE_NAME = os.getenv("JWT_COOKIE_NAME", "access_token")
COOKIE_DOMAIN = os.getenv("JWT_COOKIE_DOMAIN", "localhost")
COOKIE_SECURE = os.getenv("JWT_COOKIE_SECURE", "false").lower() == "true"
COOKIE_HTTP_ONLY = os.getenv("JWT_COOKIE_HTTP_ONLY", "true").lower() == "true"
COOKIE_SAME_SITE = os.getenv("JWT_COOKIE_SAME_SITE", "lax")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    
    Args:
        data: Data to encode in the token
        expires_delta: Token expiration time
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """
    Verify and decode a JWT token
    
    Args:
        token: JWT token to verify
        
    Returns:
        TokenData object with user information
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        token_type: str = payload.get("type")
        version: int = payload.get("version")
        
        if username is None:
            raise credentials_exception
            
        token_data = TokenData(username=username, user_id=user_id, type=token_type, version=version)  # pylint: disable=unreachable
        return token_data
        
    except JWTError as exc:
        raise credentials_exception from exc


def get_token_from_cookie(request: Request) -> Optional[str]:
    """
    Extract JWT token from HTTP-only cookie
    
    Args:
        request: FastAPI request object
        
    Returns:
        JWT token string if found, None otherwise
    """
    return request.cookies.get(COOKIE_NAME)


def get_token_from_header(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[str]:
    """
    Extract JWT token from Authorization header (for backward compatibility)
    
    Args:
        credentials: HTTP Bearer token credentials
        
    Returns:
        JWT token string if found, None otherwise
    """
    if credentials:
        return credentials.credentials
    return None


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> TokenData:
    """
    Dependency to get the current authenticated user from JWT token
    Checks both cookies and Authorization header for backward compatibility
    
    Args:
        request: FastAPI request object
        credentials: HTTP Bearer token credentials (optional)
        
    Returns:
        TokenData object with user information
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    # Try to get token from cookie first (preferred method)
    token = get_token_from_cookie(request)
    
    # Fallback to Authorization header for backward compatibility
    if not token:
        token = get_token_from_header(credentials)
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return verify_token(token)


def set_auth_cookie(response: Response, token: str, expires_delta: Optional[timedelta] = None) -> None:
    """
    Set JWT token as HTTP-only cookie
    
    Args:
        response: FastAPI response object
        token: JWT token to set
        expires_delta: Cookie expiration time
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        expires=expire,
        httponly=COOKIE_HTTP_ONLY,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAME_SITE,
        domain=COOKIE_DOMAIN if COOKIE_DOMAIN != "localhost" else None,
        path="/"
    )


def clear_auth_cookie(response: Response) -> None:
    """
    Clear JWT token cookie
    
    Args:
        response: FastAPI response object
    """
    response.delete_cookie(
        key=COOKIE_NAME,
        httponly=COOKIE_HTTP_ONLY,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAME_SITE,
        domain=COOKIE_DOMAIN if COOKIE_DOMAIN != "localhost" else None,
        path="/"
    )


async def get_current_user_from_request(request: Request) -> TokenData:
    """
    Get current user from request state (set by middleware)
    
    Args:
        request: FastAPI request object
        
    Returns:
        TokenData object with user information
        
    Raises:
        HTTPException: If user not found in request state
    """
    if not hasattr(request.state, 'current_user'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return request.state.current_user


async def get_current_active_user(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    """
    Dependency to get the current active user
    
    Args:
        current_user: Current user from JWT token
        
    Returns:
        TokenData object with user information
        
    Raises:
        HTTPException: If user is inactive
    """
    # Note: In a real application, you would check if the user is active in the database
    # For now, we assume all authenticated users are active
    return current_user


def authenticate_user(_username: str, password: str, user) -> Union[bool, dict]:
    """
    Authenticate a user with username/email and password
    
    Args:
        username: Username or email
        password: Plain text password
        user: User object from database
        
    Returns:
        False if authentication fails, user dict if successful
    """
    if not user:
        return False
    
    if not verify_password(password, user.password_hash):
        return False
    
    if not user.is_active:
        return False
    
    return user.to_response()


# Optional authentication dependency (doesn't raise exception if no token)
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[TokenData]:
    """
    Optional authentication dependency that doesn't raise exception if no token provided
    
    Args:
        credentials: HTTP Bearer token credentials (optional)
        
    Returns:
        TokenData object if valid token provided, None otherwise
    """
    if not credentials:
        return None
    
    try:
        return verify_token(credentials.credentials)
    except HTTPException:
        return None