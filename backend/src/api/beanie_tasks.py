"""
Beanie Task API endpoints for FastAPI application.
"""
# pylint: disable=no-member
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query, Depends, Request

from backend.src.models.beanie_task import BeanieTask, Label, TaskMgmtDetails
from backend.src.models.beanie_user import BeanieUser
from backend.src.api.schemas import (
    TaskCreateSchema,
    TaskUpdateSchema,
    TaskResponseSchema,
    TaskStatusUpdateSchema,
    TaskStatisticsSchema
)
from backend.src.bus_rules.auth import get_user_from_cookie, TokenData

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreateSchema, current_user: TokenData = Depends(get_user_from_cookie)):
    """
    Create a new task.
    
    Args:
        task_data: Task creation data
        
    Returns:
        Created task information
        
    Raises:
        HTTPException: If task creation fails or user not found
    """
    try:
        # Get the authenticated user
        user = await BeanieUser.find_one(BeanieUser.username == current_user.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Authenticated user not found"
            )
        
        # Create task management details if provided
        task_mgmt = None
        if task_data.priority or task_data.due_date or task_data.estimated_time:
            task_mgmt = TaskMgmtDetails(
                priority=task_data.priority or 1,
                duedate=task_data.due_date,
                estimated_time_to_complete=task_data.estimated_time
            )
        
        # Create labels if provided
        labels = []
        if task_data.labels:
            labels = [Label(name=label["name"], color=label.get("color", "#808080")) 
                     for label in task_data.labels]
        
        # Create new task
        task = BeanieTask(
            user=user,
            title=task_data.title,
            description=task_data.description or "",
            labels=labels,
            task_mgmt=task_mgmt,
            status=task_data.status or "Created"
        )
        
        # Save to database
        await task.insert()
        
        return task.to_response()
        
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
            detail=f"Failed to create task: {str(e)}"
        ) from e


@router.get("/", response_model=List[TaskResponseSchema])
async def get_tasks(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    task_status: Optional[str] = Query(None, description="Filter by task status"),
    min_priority: Optional[int] = Query(None, ge=1, le=10, description="Minimum priority"),
    max_priority: Optional[int] = Query(None, ge=1, le=10, description="Maximum priority"),
    label_name: Optional[str] = Query(None, description="Filter by label name"),
    overdue_only: bool = Query(False, description="Show only overdue tasks"),
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of tasks to return"),
    current_user: TokenData = Depends(get_user_from_cookie)
):
    """
    Retrieve tasks with optional filtering and pagination.
    
    Args:
        user_id: Filter by user ID
        task_status: Filter by task status
        min_priority: Minimum priority level
        max_priority: Maximum priority level
        label_name: Filter by label name
        overdue_only: Show only overdue tasks
        skip: Number of tasks to skip
        limit: Maximum number of tasks to return
        
    Returns:
        List of tasks
        
    Raises:
        HTTPException: If retrieval fails
    """
    try:
        # Build query
        query = {}
        
        if user_id:
            user = await BeanieUser.get(user_id)
            if user:
                query["user"] = user
            else:
                return []  # User not found, return empty list
        
        if task_status:
            query["status"] = task_status
        
        if min_priority is not None or max_priority is not None:
            priority_query = {}
            if min_priority is not None:
                priority_query["$gte"] = min_priority
            if max_priority is not None:
                priority_query["$lte"] = max_priority
            query["task_mgmt.priority"] = priority_query
        
        if label_name:
            query["labels.name"] = label_name
        
        if overdue_only:
            query["task_mgmt.duedate"] = {"$lt": datetime.now()}
        
        # Find tasks with pagination
        tasks = await BeanieTask.find(query).skip(skip).limit(limit).to_list()
        
        return [task.to_response() for task in tasks]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve tasks: {str(e)}"
        ) from e


@router.get("/{task_id}", response_model=TaskResponseSchema)
async def get_task(task_id: str, current_user: TokenData = Depends(get_user_from_cookie)):
    """
    Retrieve a specific task by ID.
    
    Args:
        task_id: Task ID
        
    Returns:
        Task information
        
    Raises:
        HTTPException: If task not found or retrieval fails
    """
    try:
        task = await BeanieTask.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID '{task_id}' not found"
            )
        
        return task.to_response()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve task: {str(e)}"
        ) from e


@router.put("/{task_id}", response_model=TaskResponseSchema)
async def update_task(task_id: str, task_data: TaskUpdateSchema, current_user: TokenData = Depends(get_user_from_cookie)):
    """
    Update an existing task.
    
    Args:
        task_id: Task ID
        task_data: Task update data
        
    Returns:
        Updated task information
        
    Raises:
        HTTPException: If task not found or update fails
    """
    try:
        # Find existing task
        task = await BeanieTask.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID '{task_id}' not found"
            )
        
        # Update task fields
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.status is not None:
            task.update_status(task_data.status)
        
        # Update labels if provided
        if task_data.labels is not None:
            task.labels = [Label(name=label["name"], color=label.get("color", "#808080")) 
                          for label in task_data.labels]
        
        # Update task management details if provided
        if task_data.priority is not None or task_data.due_date is not None or task_data.estimated_time is not None:
            if task.task_mgmt is None:
                task.task_mgmt = TaskMgmtDetails()
            
            if task_data.priority is not None:
                task.task_mgmt.priority = task_data.priority
            if task_data.due_date is not None:
                task.task_mgmt.duedate = task_data.due_date
            if task_data.estimated_time is not None:
                task.task_mgmt.estimated_time_to_complete = task_data.estimated_time
        
        # Update modification timestamp
        task.lastmoddate = datetime.now()
        
        # Save changes
        await task.save()
        
        return task.to_response()
        
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
            detail=f"Failed to update task: {str(e)}"
        ) from e


@router.patch("/{task_id}/status", response_model=TaskResponseSchema)
async def update_task_status(task_id: str, status_data: TaskStatusUpdateSchema, current_user: TokenData = Depends(get_user_from_cookie)):
    """
    Update task status.
    
    Args:
        task_id: Task ID
        status_data: Status update data
        
    Returns:
        Updated task information
        
    Raises:
        HTTPException: If task not found or status update fails
    """
    try:
        task = await BeanieTask.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID '{task_id}' not found"
            )
        
        # Update status with reason
        task.update_status(status_data.status, status_data.reason or "")
        
        # Save changes
        await task.save()
        
        return task.to_response()
        
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
            detail=f"Failed to update task status: {str(e)}"
        ) from e


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, current_user: TokenData = Depends(get_user_from_cookie)):
    """
    Delete a task.
    
    Args:
        task_id: Task ID
        
    Raises:
        HTTPException: If task not found or deletion fails
    """
    try:
        task = await BeanieTask.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID '{task_id}' not found"
            )
        
        await task.delete()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete task: {str(e)}"
        ) from e


@router.get("/user/{user_id}", response_model=List[TaskResponseSchema])
async def get_user_tasks(
    user_id: str,
    task_status: Optional[str] = Query(None, description="Filter by task status"),
    current_user: TokenData = Depends(get_user_from_cookie),
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of tasks to return")
):
    """
    Retrieve all tasks for a specific user.
    
    Args:
        user_id: User ID
        status: Filter by task status
        skip: Number of tasks to skip
        limit: Maximum number of tasks to return
        
    Returns:
        List of user's tasks
        
    Raises:
        HTTPException: If user not found or retrieval fails
    """
    try:
        # Verify user exists
        user = await BeanieUser.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID '{user_id}' not found"
            )
        
        # Build query
        query = {"user": user}
        if task_status:
            query["status"] = task_status
        
        # Find tasks with pagination
        tasks = await BeanieTask.find(query).skip(skip).limit(limit).to_list()
        
        return [task.to_response() for task in tasks]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user tasks: {str(e)}"
        ) from e


@router.get("/statistics/overview", response_model=TaskStatisticsSchema)
async def get_task_statistics(request: Request):
    """
    Get task statistics overview.
    
    Returns:
        Task statistics
        
    Raises:
        HTTPException: If statistics retrieval fails
    """
    # Manually extract user from cookie
    from backend.src.bus_rules.auth import get_token_from_cookie, verify_token
    
    token = get_token_from_cookie(request)
    print(f"DEBUG: get_task_statistics - token from cookie: {token}")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        current_user = verify_token(token)
        print(f"DEBUG: get_task_statistics called with user: {current_user}")
    except HTTPException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    
    try:
        # Get total tasks
        total_tasks = await BeanieTask.count()
        
        # Get tasks by status
        status_counts = {}
        for task_status in ["Created", "Started", "InProcess", "Modified", "Scheduled", "Complete", "Deleted"]:
            count = await BeanieTask.find(BeanieTask.status == task_status).count()
            status_counts[task_status] = count
        
        # Get overdue tasks
        overdue_count = await BeanieTask.find(
            BeanieTask.task_mgmt.duedate < datetime.now()  # type: ignore[attr-defined]
        ).count()
        
        return {
            "total": total_tasks,
            "Created": status_counts.get("Created", 0),
            "Started": status_counts.get("Started", 0),
            "InProcess": status_counts.get("InProcess", 0),
            "Modified": status_counts.get("Modified", 0),
            "Scheduled": status_counts.get("Scheduled", 0),
            "Complete": status_counts.get("Complete", 0),
            "Deleted": status_counts.get("Deleted", 0),
            "overdue": overdue_count
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve task statistics: {str(e)}"
        ) from e
