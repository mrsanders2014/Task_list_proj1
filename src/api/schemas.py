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
