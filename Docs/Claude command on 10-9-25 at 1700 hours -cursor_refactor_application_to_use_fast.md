# Refactor application to use fastapi
_Exported on 10/9/2025 at 17:06:00 EDT from Cursor (1.7.40)_

---

**User**

I need to refactor this application to no longer utilize the CLI commands or any of those files. Instead, we want to leverage fastapi to make all of our requests to our API through HTTP, you know, get, post, put and delete. For all CRUD operations, related to user and task.  Adjust the code to accommodate

---

**Cursor**

I'll help you refactor this application from a CLI-based system to a FastAPI-based HTTP API. Let me first examine the current codebase structure to understand what needs to be changed.


Now I understand the current structure. The application has:

1. **CLI Interface** (`src/User_int/cli.py`) - This needs to be removed
2. **Models** (`src/model/user.py`, `src/model/task.py`) - These are good and can be reused
3. **Repositories** (`src/dbase/user_repository.py`, `src/dbase/task_repository.py`) - These are good and can be reused
4. **Database Connection** (`src/dbase/connection.py`) - This is good and can be reused
5. **FastAPI is already in dependencies** - Great!

Let me start by setting up the FastAPI application and creating the API endpoints.


First, let me create the FastAPI application structure. I'll create API routers for users and tasks:


```python
"""
API package for FastAPI application.
"""
```

```python
"""
Pydantic schemas for API request/response models.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr, validator


class LabelSchema(BaseModel):
    """Label schema for API."""
    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="#808080", regex="^#[0-9A-Fa-f]{6}$")


class TaskMgmtDetailsSchema(BaseModel):
    """Task management details schema for API."""
    priority: int = Field(default=1, ge=1, le=10)
    duedate: Optional[datetime] = None
    time_unit: str = Field(default="hours", regex="^(minutes|hours|days|weeks|months|years)$")
    estimated_time_to_complete: Optional[float] = Field(None, ge=1)
    notify_time: float = Field(default=0, ge=0)
    notify_time_units: str = Field(default="hours", regex="^(minutes|hours|days|weeks|months|years)$")
    notification_wanted: str = Field(default="N", regex="^[YN]$")


class TaskCreateSchema(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=50)
    description: str = Field(default="", max_length=250)
    labels: Optional[List[LabelSchema]] = None
    task_mgmt: Optional[TaskMgmtDetailsSchema] = None
    status: str = Field(default="Created", regex="^(Created|Started|InProcess|Modified|Scheduled|Complete|Deleted)$")


class TaskUpdateSchema(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=250)
    labels: Optional[List[LabelSchema]] = None
    task_mgmt: Optional[TaskMgmtDetailsSchema] = None
    status: Optional[str] = Field(None, regex="^(Created|Started|InProcess|Modified|Scheduled|Complete|Deleted)$")


class TaskResponseSchema(BaseModel):
    """Schema for task response."""
    id: str
    user_id: str
    title: str
    description: str
    labels: List[Dict[str, str]]
    task_mgmt: Optional[Dict[str, Any]]
    status: str
    createdate: datetime
    lastmoddate: datetime

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    """Schema for creating a new user."""
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)


class UserUpdateSchema(BaseModel):
    """Schema for updating a user."""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None


class UserResponseSchema(BaseModel):
    """Schema for user response."""
    id: str
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: str
    created_at: datetime
    updated_at: Optional[datetime]
    last_login: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True


class TaskStatusUpdateSchema(BaseModel):
    """Schema for updating task status."""
    status: str = Field(..., regex="^(Created|Started|InProcess|Modified|Scheduled|Complete|Deleted)$")
    reason: str = Field(default="", max_length=250)


class TaskStatisticsSchema(BaseModel):
    """Schema for task statistics response."""
    total: int
    Created: int
    Started: int
    InProcess: int
    Modified: int
    Scheduled: int
    Complete: int
    Deleted: int
    overdue: int


class ErrorResponseSchema(BaseModel):
    """Schema for error responses."""
    detail: str
    error_code: Optional[str] = None
```

```python
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
    UserResponseSchema,
    ErrorResponseSchema
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
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )


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
        )


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
        )


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
        )


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
            if existing_email and existing_email._id != user._id:
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
        )


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
        )


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
        )
```

```python
"""
Task API endpoints for FastAPI application.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Query, Path
from fastapi.responses import JSONResponse

from src.model.task import Task, Label, TaskMgmtDetails
from src.dbase.task_repository import TaskRepository
from src.dbase.user_repository import UserRepository
from src.api.schemas import (
    TaskCreateSchema,
    TaskUpdateSchema,
    TaskResponseSchema,
    TaskStatusUpdateSchema,
    TaskStatisticsSchema,
    ErrorResponseSchema
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _convert_task_to_response(task: Task) -> dict:
    """Convert Task model to response format."""
    return {
        "id": str(task._id) if task._id else None,
        "user_id": task.user_id,
        "title": task.title,
        "description": task.description,
        "labels": [{"name": label.name, "color": label.color} for label in task.labels] if task.labels else [],
        "task_mgmt": task.task_mgmt.to_dict() if task.task_mgmt else None,
        "status": task.status,
        "createdate": task.createdate,
        "lastmoddate": task.lastmoddate
    }


@router.post("/", response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreateSchema, user_id: str = Query(..., description="User ID who owns this task")):
    """
    Create a new task.
    
    Args:
        task_data: Task creation data
        user_id: User ID who owns this task
        
    Returns:
        Created task information
        
    Raises:
        HTTPException: If task creation fails
    """
    try:
        # Verify user exists
        user_repo = UserRepository()
        user = user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID '{user_id}' not found"
            )
        
        # Convert labels
        labels = []
        if task_data.labels:
            labels = [Label(label.name, label.color) for label in task_data.labels]
        
        # Convert task management details
        task_mgmt = None
        if task_data.task_mgmt:
            task_mgmt = TaskMgmtDetails(
                priority=task_data.task_mgmt.priority,
                duedate=task_data.task_mgmt.duedate,
                time_unit=task_data.task_mgmt.time_unit,
                estimated_time_to_complete=task_data.task_mgmt.estimated_time_to_complete,
                notify_time=task_data.task_mgmt.notify_time,
                notify_time_units=task_data.task_mgmt.notify_time_units,
                notification_wanted=task_data.task_mgmt.notification_wanted
            )
        
        # Create task
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            labels=labels,
            task_mgmt=task_mgmt,
            status=task_data.status
        )
        
        task_repo = TaskRepository()
        task_id = task_repo.create(task)
        task._id = task_id
        
        return _convert_task_to_response(task)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task: {str(e)}"
        )


@router.get("/", response_model=List[TaskResponseSchema])
async def get_tasks(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    status: Optional[str] = Query(None, description="Filter by task status"),
    min_priority: Optional[int] = Query(None, ge=1, le=10, description="Minimum priority"),
    max_priority: Optional[int] = Query(None, ge=1, le=10, description="Maximum priority"),
    label_name: Optional[str] = Query(None, description="Filter by label name"),
    overdue_only: bool = Query(False, description="Show only overdue tasks")
):
    """
    Get tasks with optional filters.
    
    Args:
        user_id: Filter by user ID
        status: Filter by task status
        min_priority: Minimum priority level
        max_priority: Maximum priority level
        label_name: Filter by label name
        overdue_only: Show only overdue tasks
        
    Returns:
        List of tasks
    """
    try:
        task_repo = TaskRepository()
        
        if not user_id:
            # Get all tasks if no user_id specified
            tasks = task_repo.get_all()
        elif overdue_only:
            tasks = task_repo.get_overdue_tasks(user_id)
        elif min_priority is not None and max_priority is not None:
            tasks = task_repo.get_by_priority(user_id, min_priority, max_priority)
        elif label_name:
            tasks = task_repo.get_by_label(user_id, label_name)
        else:
            tasks = task_repo.get_by_user(user_id, status=status)
        
        return [_convert_task_to_response(task) for task in tasks]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve tasks: {str(e)}"
        )


@router.get("/{task_id}", response_model=TaskResponseSchema)
async def get_task(task_id: str = Path(..., description="Task ID")):
    """
    Get a task by ID.
    
    Args:
        task_id: Task's MongoDB ObjectId
        
    Returns:
        Task information
        
    Raises:
        HTTPException: If task not found
    """
    try:
        task_repo = TaskRepository()
        task = task_repo.get_by_id(task_id)
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID '{task_id}' not found"
            )
        
        return _convert_task_to_response(task)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve task: {str(e)}"
        )


@router.put("/{task_id}", response_model=TaskResponseSchema)
async def update_task(
    task_id: str = Path(..., description="Task ID"),
    task_data: TaskUpdateSchema = None
):
    """
    Update a task's information.
    
    Args:
        task_id: Task's MongoDB ObjectId
        task_data: Task update data
        
    Returns:
        Updated task information
        
    Raises:
        HTTPException: If task not found or update fails
    """
    try:
        task_repo = TaskRepository()
        
        # Check if task exists
        task = task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID '{task_id}' not found"
            )
        
        # Prepare update data
        update_data = {}
        
        if task_data.title is not None:
            update_data["title"] = task_data.title
        
        if task_data.description is not None:
            update_data["description"] = task_data.description
        
        if task_data.labels is not None:
            labels = [Label(label.name, label.color) for label in task_data.labels]
            update_data["labels"] = [label.to_dict() for label in labels]
        
        if task_data.task_mgmt is not None:
            task_mgmt = TaskMgmtDetails(
                priority=task_data.task_mgmt.priority,
                duedate=task_data.task_mgmt.duedate,
                time_unit=task_data.task_mgmt.time_unit,
                estimated_time_to_complete=task_data.task_mgmt.estimated_time_to_complete,
                notify_time=task_data.task_mgmt.notify_time,
                notify_time_units=task_data.task_mgmt.notify_time_units,
                notification_wanted=task_data.task_mgmt.notification_wanted
            )
            update_data["task_mgmt"] = task_mgmt.to_dict()
        
        # Update task
        if update_data:
            success = task_repo.update(task_id, update_data)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update task"
                )
        
        # Return updated task
        updated_task = task_repo.get_by_id(task_id)
        return _convert_task_to_response(updated_task)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update task: {str(e)}"
        )


@router.patch("/{task_id}/status", response_model=TaskResponseSchema)
async def update_task_status(
    task_id: str = Path(..., description="Task ID"),
    status_data: TaskStatusUpdateSchema = None
):
    """
    Update a task's status.
    
    Args:
        task_id: Task's MongoDB ObjectId
        status_data: Status update data
        
    Returns:
        Updated task information
        
    Raises:
        HTTPException: If task not found or update fails
    """
    try:
        task_repo = TaskRepository()
        
        # Check if task exists
        task = task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID '{task_id}' not found"
            )
        
        # Update status
        success = task_repo.update_status(task_id, status_data.status, status_data.reason)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update task status"
            )
        
        # Return updated task
        updated_task = task_repo.get_by_id(task_id)
        return _convert_task_to_response(updated_task)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update task status: {str(e)}"
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str = Path(..., description="Task ID"),
    soft_delete: bool = Query(True, description="Perform soft delete (set status to Deleted)"),
    reason: str = Query("User deleted", description="Reason for deletion")
):
    """
    Delete a task.
    
    Args:
        task_id: Task's MongoDB ObjectId
        soft_delete: Whether to perform soft delete
        reason: Reason for deletion
        
    Raises:
        HTTPException: If task not found or deletion fails
    """
    try:
        task_repo = TaskRepository()
        
        # Check if task exists
        task = task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID '{task_id}' not found"
            )
        
        # Delete task
        if soft_delete:
            success = task_repo.soft_delete(task_id, reason)
        else:
            success = task_repo.delete(task_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete task"
            )
        
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete task: {str(e)}"
        )


@router.get("/user/{user_id}/statistics", response_model=TaskStatisticsSchema)
async def get_task_statistics(user_id: str = Path(..., description="User ID")):
    """
    Get task statistics for a user.
    
    Args:
        user_id: User's MongoDB ObjectId
        
    Returns:
        Task statistics
        
    Raises:
        HTTPException: If user not found or statistics retrieval fails
    """
    try:
        # Verify user exists
        user_repo = UserRepository()
        user = user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID '{user_id}' not found"
            )
        
        task_repo = TaskRepository()
        stats = task_repo.get_task_statistics(user_id)
        
        return TaskStatisticsSchema(**stats)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve task statistics: {str(e)}"
        )
```

```python
"""
Main FastAPI application setup.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from src.api.users import router as users_router
from src.api.tasks import router as tasks_router
from src.settings import Setup

# Initialize FastAPI app
app = FastAPI(
    title="Task Manager API",
    description="A RESTful API for managing users and tasks",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users_router)
app.include_router(tasks_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup."""
    try:
        MONGO_URI, DB_NAME = Setup()
        print(f"✓ Database connection initialized")
        print(f"✓ MongoDB URI: {MONGO_URI}")
        print(f"✓ Database Name: {DB_NAME}")
    except Exception as e:
        print(f"⚠ Warning: Database connection failed: {e}")
        print("⚠ Running in mock mode")


@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Task Manager API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "users": "/users",
            "tasks": "/tasks"
        }
    }


@app.get("/health", response_model=dict)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "Task Manager API is running"
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_code": "INTERNAL_ERROR"
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
```

Now let me update the main.py file to serve the FastAPI application instead of the CLI:


```python
"""
Task Manager FastAPI Application
Main entry point for the FastAPI application.
"""
import uvicorn
from src.api.main import app
from src.settings import Setup


def main():
    """Main entry point for the FastAPI application."""
    try:
        MONGO_URI, DB_NAME = Setup()
        print(f"✓ MongoDB URI: {MONGO_URI}")
        print(f"✓ Database Name: {DB_NAME}")
        print("✓ Launching Task Manager FastAPI application...")
        print("✓ API Documentation available at: http://localhost:8000/docs")
        print("✓ Alternative docs at: http://localhost:8000/redoc")
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        print(f"✗ Failed to start application: {e}")
        raise


if __name__ == "__main__":
    main()

```

Now let me remove the CLI-related files and components:


---

**User**

continue?

---

**Cursor**



Let me check the current dependencies and add any missing ones for the FastAPI application:


I need to add `email-validator` for the `EmailStr` type used in the schemas, and remove `rich` since we're no longer using the CLI:


```toml
[project]
name = "task-list-proj1"
dynamic = ["version"]  # Remove static version and add this line
# version = "0.1.0"
description = "Application to allow user to create and track tasks"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "beanie>=2.0.0",
    "black>=25.9.0",
    "email-validator>=2.0.0",
    "fastapi>=0.118.2",
    "motor[sdam]>=3.7.1",
    "mypy>=1.18.2",
    "pylint>=3.3.8",
    "pymongo>=4.15.2",
    "pytest>=8.4.2",
    "python-dotenv>=1.1.1",
    "ruff>=0.13.3",
    "uvicorn>=0.37.0",
]

[build-system]
requires = ["hatchling", "uv-dynamic-versioning"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src"]

[tool.hatch.version]
source = "uv-dynamic-versioning"

```

Now let me check for any linting errors in the new API files and fix them:


Let me also check the main.py file:


Now let me test the FastAPI application by running it to make sure everything works:


Great! Now let me test the FastAPI application by starting it briefly to make sure it works:


Let me try a different approach to test the application:


I need to fix the Pydantic schema - the `regex` parameter has been replaced with `pattern` in Pydantic v2. Let me update the schemas:


```python
"""
Pydantic schemas for API request/response models.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr, validator


class LabelSchema(BaseModel):
    """Label schema for API."""
    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="#808080", pattern="^#[0-9A-Fa-f]{6}$")


class TaskMgmtDetailsSchema(BaseModel):
    """Task management details schema for API."""
    priority: int = Field(default=1, ge=1, le=10)
    duedate: Optional[datetime] = None
    time_unit: str = Field(default="hours", regex="^(minutes|hours|days|weeks|months|years)$")
    estimated_time_to_complete: Optional[float] = Field(None, ge=1)
    notify_time: float = Field(default=0, ge=0)
    notify_time_units: str = Field(default="hours", regex="^(minutes|hours|days|weeks|months|years)$")
    notification_wanted: str = Field(default="N", regex="^[YN]$")


class TaskCreateSchema(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=50)
    description: str = Field(default="", max_length=250)
    labels: Optional[List[LabelSchema]] = None
    task_mgmt: Optional[TaskMgmtDetailsSchema] = None
    status: str = Field(default="Created", regex="^(Created|Started|InProcess|Modified|Scheduled|Complete|Deleted)$")


class TaskUpdateSchema(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=250)
    labels: Optional[List[LabelSchema]] = None
    task_mgmt: Optional[TaskMgmtDetailsSchema] = None
    status: Optional[str] = Field(None, regex="^(Created|Started|InProcess|Modified|Scheduled|Complete|Deleted)$")


class TaskResponseSchema(BaseModel):
    """Schema for task response."""
    id: str
    user_id: str
    title: str
    description: str
    labels: List[Dict[str, str]]
    task_mgmt: Optional[Dict[str, Any]]
    status: str
    createdate: datetime
    lastmoddate: datetime

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    """Schema for creating a new user."""
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)


class UserUpdateSchema(BaseModel):
    """Schema for updating a user."""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None


class UserResponseSchema(BaseModel):
    """Schema for user response."""
    id: str
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: str
    created_at: datetime
    updated_at: Optional[datetime]
    last_login: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True


class TaskStatusUpdateSchema(BaseModel):
    """Schema for updating task status."""
    status: str = Field(..., regex="^(Created|Started|InProcess|Modified|Scheduled|Complete|Deleted)$")
    reason: str = Field(default="", max_length=250)


class TaskStatisticsSchema(BaseModel):
    """Schema for task statistics response."""
    total: int
    Created: int
    Started: int
    InProcess: int
    Modified: int
    Scheduled: int
    Complete: int
    Deleted: int
    overdue: int


class ErrorResponseSchema(BaseModel):
    """Schema for error responses."""
    detail: str
    error_code: Optional[str] = None

```

```python
"""
Pydantic schemas for API request/response models.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr, validator


class LabelSchema(BaseModel):
    """Label schema for API."""
    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="#808080", pattern="^#[0-9A-Fa-f]{6}$")


class TaskMgmtDetailsSchema(BaseModel):
    """Task management details schema for API."""
    priority: int = Field(default=1, ge=1, le=10)
    duedate: Optional[datetime] = None
    time_unit: str = Field(default="hours", pattern="^(minutes|hours|days|weeks|months|years)$")
    estimated_time_to_complete: Optional[float] = Field(None, ge=1)
    notify_time: float = Field(default=0, ge=0)
    notify_time_units: str = Field(default="hours", pattern="^(minutes|hours|days|weeks|months|years)$")
    notification_wanted: str = Field(default="N", pattern="^[YN]$")


class TaskCreateSchema(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=50)
    description: str = Field(default="", max_length=250)
    labels: Optional[List[LabelSchema]] = None
    task_mgmt: Optional[TaskMgmtDetailsSchema] = None
    status: str = Field(default="Created", regex="^(Created|Started|InProcess|Modified|Scheduled|Complete|Deleted)$")


class TaskUpdateSchema(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=250)
    labels: Optional[List[LabelSchema]] = None
    task_mgmt: Optional[TaskMgmtDetailsSchema] = None
    status: Optional[str] = Field(None, regex="^(Created|Started|InProcess|Modified|Scheduled|Complete|Deleted)$")


class TaskResponseSchema(BaseModel):
    """Schema for task response."""
    id: str
    user_id: str
    title: str
    description: str
    labels: List[Dict[str, str]]
    task_mgmt: Optional[Dict[str, Any]]
    status: str
    createdate: datetime
    lastmoddate: datetime

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    """Schema for creating a new user."""
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)


class UserUpdateSchema(BaseModel):
    """Schema for updating a user."""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None


class UserResponseSchema(BaseModel):
    """Schema for user response."""
    id: str
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: str
    created_at: datetime
    updated_at: Optional[datetime]
    last_login: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True


class TaskStatusUpdateSchema(BaseModel):
    """Schema for updating task status."""
    status: str = Field(..., regex="^(Created|Started|InProcess|Modified|Scheduled|Complete|Deleted)$")
    reason: str = Field(default="", max_length=250)


class TaskStatisticsSchema(BaseModel):
    """Schema for task statistics response."""
    total: int
    Created: int
    Started: int
    InProcess: int
    Modified: int
    Scheduled: int
    Complete: int
    Deleted: int
    overdue: int


class ErrorResponseSchema(BaseModel):
    """Schema for error responses."""
    detail: str
    error_code: Optional[str] = None

```

```python
"""
Pydantic schemas for API request/response models.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr, validator


class LabelSchema(BaseModel):
    """Label schema for API."""
    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="#808080", pattern="^#[0-9A-Fa-f]{6}$")


class TaskMgmtDetailsSchema(BaseModel):
    """Task management details schema for API."""
    priority: int = Field(default=1, ge=1, le=10)
    duedate: Optional[datetime] = None
    time_unit: str = Field(default="hours", pattern="^(minutes|hours|days|weeks|months|years)$")
    estimated_time_to_complete: Optional[float] = Field(None, ge=1)
    notify_time: float = Field(default=0, ge=0)
    notify_time_units: str = Field(default="hours", pattern="^(minutes|hours|days|weeks|months|years)$")
    notification_wanted: str = Field(default="N", pattern="^[YN]$")


class TaskCreateSchema(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=50)
    description: str = Field(default="", max_length=250)
    labels: Optional[List[LabelSchema]] = None
    task_mgmt: Optional[TaskMgmtDetailsSchema] = None
    status: str = Field(default="Created", pattern="^(Created|Started|InProcess|Modified|Scheduled|Complete|Deleted)$")


class TaskUpdateSchema(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=250)
    labels: Optional[List[LabelSchema]] = None
    task_mgmt: Optional[TaskMgmtDetailsSchema] = None
    status: Optional[str] = Field(None, regex="^(Created|Started|InProcess|Modified|Scheduled|Complete|Deleted)$")


class TaskResponseSchema(BaseModel):
    """Schema for task response."""
    id: str
    user_id: str
    title: str
    description: str
    labels: List[Dict[str, str]]
    task_mgmt: Optional[Dict[str, Any]]
    status: str
    createdate: datetime
    lastmoddate: datetime

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    """Schema for creating a new user."""
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)


class UserUpdateSchema(BaseModel):
    """Schema for updating a user."""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None


class UserResponseSchema(BaseModel):
    """Schema for user response."""
    id: str
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: str
    created_at: datetime
    updated_at: Optional[datetime]
    last_login: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True


class TaskStatusUpdateSchema(BaseModel):
    """Schema for updating task status."""
    status: str = Field(..., regex="^(Created|Started|InProcess|Modified|Scheduled|Complete|Deleted)$")
    reason: str = Field(default="", max_length=250)


class TaskStatisticsSchema(BaseModel):
    """Schema for task statistics response."""
    total: int
    Created: int
    Started: int
    InProcess: int
    Modified: int
    Scheduled: int
    Complete: int
    Deleted: int
    overdue: int


class ErrorResponseSchema(BaseModel):
    """Schema for error responses."""
    detail: str
    error_code: Optional[str] = None

```

```python
"""
Pydantic schemas for API request/response models.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr, validator


class LabelSchema(BaseModel):
    """Label schema for API."""
    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="#808080", pattern="^#[0-9A-Fa-f]{6}$")


class TaskMgmtDetailsSchema(BaseModel):
    """Task management details schema for API."""
    priority: int = Field(default=1, ge=1, le=10)
    duedate: Optional[datetime] = None
    time_unit: str = Field(default="hours", pattern="^(minutes|hours|days|weeks|months|years)$")
    estimated_time_to_complete: Optional[float] = Field(None, ge=1)
    notify_time: float = Field(default=0, ge=0)
    notify_time_units: str = Field(default="hours", pattern="^(minutes|hours|days|weeks|months|years)$")
    notification_wanted: str = Field(default="N", pattern="^[YN]$")


class TaskCreateSchema(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=50)
    description: str = Field(default="", max_length=250)
    labels: Optional[List[LabelSchema]] = None
    task_mgmt: Optional[TaskMgmtDetailsSchema] = None
    status: str = Field(default="Created", pattern="^(Created|Started|InProcess|Modified|Scheduled|Complete|Deleted)$")


class TaskUpdateSchema(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=250)
    labels: Optional[List[LabelSchema]] = None
    task_mgmt: Optional[TaskMgmtDetailsSchema] = None
    status: Optional[str] = Field(None, pattern="^(Created|Started|InProcess|Modified|Scheduled|Complete|Deleted)$")


class TaskResponseSchema(BaseModel):
    """Schema for task response."""
    id: str
    user_id: str
    title: str
    description: str
    labels: List[Dict[str, str]]
    task_mgmt: Optional[Dict[str, Any]]
    status: str
    createdate: datetime
    lastmoddate: datetime

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    """Schema for creating a new user."""
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)


class UserUpdateSchema(BaseModel):
    """Schema for updating a user."""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None


class UserResponseSchema(BaseModel):
    """Schema for user response."""
    id: str
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: str
    created_at: datetime
    updated_at: Optional[datetime]
    last_login: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True


class TaskStatusUpdateSchema(BaseModel):
    """Schema for updating task status."""
    status: str = Field(..., regex="^(Created|Started|InProcess|Modified|Scheduled|Complete|Deleted)$")
    reason: str = Field(default="", max_length=250)


class TaskStatisticsSchema(BaseModel):
    """Schema for task statistics response."""
    total: int
    Created: int
    Started: int
    InProcess: int
    Modified: int
    Scheduled: int
    Complete: int
    Deleted: int
    overdue: int


class ErrorResponseSchema(BaseModel):
    """Schema for error responses."""
    detail: str
    error_code: Optional[str] = None

```

```python
"""
Pydantic schemas for API request/response models.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr, validator


class LabelSchema(BaseModel):
    """Label schema for API."""
    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="#808080", pattern="^#[0-9A-Fa-f]{6}$")


class TaskMgmtDetailsSchema(BaseModel):
    """Task management details schema for API."""
    priority: int = Field(default=1, ge=1, le=10)
    duedate: Optional[datetime] = None
    time_unit: str = Field(default="hours", pattern="^(minutes|hours|days|weeks|months|years)$")
    estimated_time_to_complete: Optional[float] = Field(None, ge=1)
    notify_time: float = Field(default=0, ge=0)
    notify_time_units: str = Field(default="hours", pattern="^(minutes|hours|days|weeks|months|years)$")
    notification_wanted: str = Field(default="N", pattern="^[YN]$")


class TaskCreateSchema(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=50)
    description: str = Field(default="", max_length=250)
    labels: Optional[List[LabelSchema]] = None
    task_mgmt: Optional[TaskMgmtDetailsSchema] = None
    status: str = Field(default="Created", pattern="^(Created|Started|InProcess|Modified|Scheduled|Complete|Deleted)$")


class TaskUpdateSchema(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=250)
    labels: Optional[List[LabelSchema]] = None
    task_mgmt: Optional[TaskMgmtDetailsSchema] = None
    status: Optional[str] = Field(None, pattern="^(Created|Started|InProcess|Modified|Scheduled|Complete|Deleted)$")


class TaskResponseSchema(BaseModel):
    """Schema for task response."""
    id: str
    user_id: str
    title: str
    description: str
    labels: List[Dict[str, str]]
    task_mgmt: Optional[Dict[str, Any]]
    status: str
    createdate: datetime
    lastmoddate: datetime

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    """Schema for creating a new user."""
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)


class UserUpdateSchema(BaseModel):
    """Schema for updating a user."""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None


class UserResponseSchema(BaseModel):
    """Schema for user response."""
    id: str
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: str
    created_at: datetime
    updated_at: Optional[datetime]
    last_login: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True


class TaskStatusUpdateSchema(BaseModel):
    """Schema for updating task status."""
    status: str = Field(..., pattern="^(Created|Started|InProcess|Modified|Scheduled|Complete|Deleted)$")
    reason: str = Field(default="", max_length=250)


class TaskStatisticsSchema(BaseModel):
    """Schema for task statistics response."""
    total: int
    Created: int
    Started: int
    InProcess: int
    Modified: int
    Scheduled: int
    Complete: int
    Deleted: int
    overdue: int


class ErrorResponseSchema(BaseModel):
    """Schema for error responses."""
    detail: str
    error_code: Optional[str] = None

```

Now let me test the import again:


Excellent! Now let me create a simple README file to document how to use the new FastAPI application:


```markdown
# Task Manager FastAPI Application

This application has been refactored from a CLI-based system to a RESTful API using FastAPI.

## Features

- **User Management**: Create, read, update, and delete users
- **Task Management**: Full CRUD operations for tasks with advanced filtering
- **Task Statistics**: Get comprehensive statistics for user tasks
- **Status Management**: Update task status with history tracking
- **Priority & Label Support**: Organize tasks with priorities and labels
- **Due Date Management**: Set due dates and track overdue tasks

## Quick Start

### 1. Install Dependencies

```bash
pip install -e .
```

### 2. Start the Application

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### 3. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/` | Create a new user |
| GET | `/users/` | Get all users (with optional filters) |
| GET | `/users/{user_id}` | Get user by ID |
| GET | `/users/username/{username}` | Get user by username |
| PUT | `/users/{user_id}` | Update user information |
| DELETE | `/users/{user_id}` | Delete a user |
| PATCH | `/users/{user_id}/status` | Change user active status |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks/` | Create a new task |
| GET | `/tasks/` | Get tasks (with optional filters) |
| GET | `/tasks/{task_id}` | Get task by ID |
| PUT | `/tasks/{task_id}` | Update task information |
| PATCH | `/tasks/{task_id}/status` | Update task status |
| DELETE | `/tasks/{task_id}` | Delete a task (soft or hard) |
| GET | `/tasks/user/{user_id}/statistics` | Get task statistics for user |

### Query Parameters for GET /tasks/

- `user_id`: Filter by user ID
- `status`: Filter by task status
- `min_priority`: Minimum priority level (1-10)
- `max_priority`: Maximum priority level (1-10)
- `label_name`: Filter by label name
- `overdue_only`: Show only overdue tasks (true/false)

## Example Usage

### Create a User

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Create a Task

```bash
curl -X POST "http://localhost:8000/tasks/?user_id=USER_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive API documentation",
    "status": "Created",
    "task_mgmt": {
      "priority": 3,
      "time_unit": "hours",
      "estimated_time_to_complete": 4.0
    },
    "labels": [
      {
        "name": "documentation",
        "color": "#3498db"
      }
    ]
  }'
```

### Get User Tasks

```bash
curl "http://localhost:8000/tasks/?user_id=USER_ID"
```

### Update Task Status

```bash
curl -X PATCH "http://localhost:8000/tasks/TASK_ID/status" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "InProcess",
    "reason": "Started working on the task"
  }'
```

### Get Task Statistics

```bash
curl "http://localhost:8000/tasks/user/USER_ID/statistics"
```

## Data Models

### User Schema

```json
{
  "username": "string",
  "email": "string",
  "first_name": "string (optional)",
  "last_name": "string (optional)"
}
```

### Task Schema

```json
{
  "title": "string (max 50 chars)",
  "description": "string (max 250 chars, optional)",
  "status": "Created|Started|InProcess|Modified|Scheduled|Complete|Deleted",
  "labels": [
    {
      "name": "string",
      "color": "#hexcolor"
    }
  ],
  "task_mgmt": {
    "priority": 1-10,
    "duedate": "datetime (optional)",
    "time_unit": "minutes|hours|days|weeks|months|years",
    "estimated_time_to_complete": "number (optional)",
    "notify_time": "number",
    "notify_time_units": "minutes|hours|days|weeks|months|years",
    "notification_wanted": "Y|N"
  }
}
```

## Configuration

The application uses environment variables for configuration:

- `MONGO_URI`: MongoDB connection string
- `DB_NAME`: Database name

Create a `.env` file in the project root:

```
MONGO_URI=mongodb://localhost:27017
DB_NAME=task_manager
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black src/
ruff check src/
```

### Type Checking

```bash
mypy src/
```

## Migration from CLI

The application has been completely refactored from CLI to API:

- ✅ Removed CLI interface (`src/User_int/cli.py`)
- ✅ Created FastAPI application with full CRUD endpoints
- ✅ Maintained all existing data models and repositories
- ✅ Added comprehensive API documentation
- ✅ Implemented proper error handling and validation
- ✅ Added CORS support for web frontend integration

All existing functionality is now available through HTTP endpoints with proper REST conventions.
```

Perfect! I have successfully refactored your application from a CLI-based system to a FastAPI-based HTTP API. Here's a summary of what was accomplished:

## ✅ **Refactoring Complete**

### **What Was Changed:**

1. **Removed CLI Components:**
   - Deleted `src/User_int/cli.py` and the entire `User_int` directory
   - Removed `rich` dependency (no longer needed for CLI)

2. **Created FastAPI Application:**
   - **`src/api/main.py`** - Main FastAPI application with CORS support
   - **`src/api/schemas.py`** - Pydantic schemas for request/response validation
   - **`src/api/users.py`** - User CRUD endpoints
   - **`src/api/tasks.py`** - Task CRUD endpoints

3. **Updated Dependencies:**
   - Added `email-validator` for email validation
   - Removed `rich` (CLI library)
   - All FastAPI dependencies were already present

4. **Updated Entry Point:**
   - Modified `main.py` to serve FastAPI application instead of CLI

### **API Endpoints Available:**

#### **Users:**
- `POST /users/` - Create user
- `GET /users/` - Get all users
- `GET /users/{user_id}` - Get user by ID
- `GET /users/username/{username}` - Get user by username
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user
- `PATCH /users/{user_id}/status` - Change user status

#### **Tasks:**
- `POST /tasks/` - Create task
- `GET /tasks/` - Get tasks (with filters)
- `GET /tasks/{task_id}` - Get task by ID
- `PUT /tasks/{task_id}` - Update task
- `PATCH /tasks/{task_id}/status` - Update task status
- `DELETE /tasks/{task_id}` - Delete task
- `GET /tasks/user/{user_id}/statistics` - Get task statistics

### **How to Use:**

1. **Start the API:**
   ```bash
   python main.py
   ```

2. **Access Documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Make HTTP Requests:**
   ```bash
   # Create a user
   curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{"username": "john", "email": "john@example.com"}'
   
   # Create a task
   curl -X POST "http://localhost:8000/tasks/?user_id=USER_ID" \
     -H "Content-Type: application/json" \
     -d '{"title": "My Task", "description": "Task description"}'
   ```

### **Key Features:**
- ✅ Full CRUD operations for users and tasks
- ✅ Advanced task filtering (by status, priority, labels, overdue)
- ✅ Task statistics and status management
- ✅ Comprehensive API documentation
- ✅ Proper error handling and validation
- ✅ CORS support for web frontend integration
- ✅ Maintained all existing data models and repositories

The application is now ready to be used as a RESTful API instead of a CLI application. All the existing functionality has been preserved and enhanced with proper HTTP endpoints, validation, and documentation.

```shellscript
   python main.py
```

```shellscript
   # Create a user
   curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{"username": "john", "email": "john@example.com"}'
   
   # Create a task
   curl -X POST "http://localhost:8000/tasks/?user_id=USER_ID" \
     -H "Content-Type: application/json" \
     -d '{"title": "My Task", "description": "Task description"}'
```

