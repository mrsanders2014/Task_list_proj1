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
    TaskStatisticsSchema
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
        
        # Get the created task with ID
        created_task = task_repo.get_by_id(task_id)
        return _convert_task_to_response(created_task)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e
    except HTTPException:
        raise
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
    overdue_only: bool = Query(False, description="Show only overdue tasks")
):
    """
    Get tasks with optional filters.
    
    Args:
        user_id: Filter by user ID
        task_status: Filter by task status
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
            tasks = task_repo.get_by_user(user_id, status=task_status)
        
        return [_convert_task_to_response(task) for task in tasks]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve tasks: {str(e)}"
        ) from e


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
        ) from e


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
        ) from e


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
        ) from e


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
        ) from e


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
        ) from e
