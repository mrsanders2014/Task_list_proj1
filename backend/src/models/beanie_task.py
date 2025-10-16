"""
Beanie Task Document Model
Defines the Task document structure using Beanie ODM.
"""
# pylint: disable=no-member
from datetime import datetime, timedelta
from typing import Optional, List, ClassVar
from beanie import Document, Link
from pydantic import Field, field_validator, BaseModel
from pymongo import IndexModel

from backend.src.models.beanie_user import BeanieUser


class Label(BaseModel):
    """Label model for task categorization."""
    
    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="#808080")
    
    def __str__(self) -> str:
        return f"{self.name} ({self.color})"


class TaskTimeMgmt(BaseModel):
    """Task time management details."""
    
    create_date: Optional[datetime] = Field(default_factory=datetime.now)
    scheduled_start_date: Optional[datetime] = Field(None)
    actual_start_date: Optional[datetime] = Field(None)
    scheduled_comp_date: Optional[datetime] = Field(None)
    actual_comp_date: Optional[datetime] = Field(None)
    archived_date: Optional[datetime] = Field(None)


class TaskMgmtDetails(BaseModel):
    """Task management details including priority, deadlines, and notifications."""
    
    VALID_TIME_UNITS: ClassVar[List[str]] = ["minutes", "hours", "days", "weeks", "months", "years"]
    
    priority: int = Field(default=1, ge=1, le=10)
    duedate: Optional[datetime] = Field(None)
    time_unit: str = Field(default="hours")
    estimated_time_to_complete: Optional[float] = Field(None, ge=1)
    notify_time: float = Field(default=0, ge=0)
    notify_time_units: str = Field(default="hours")
    notification_wanted: str = Field(default="N")
    time_mgmt: List[TaskTimeMgmt] = Field(default_factory=list)
    
    @field_validator('time_unit', 'notify_time_units')
    @classmethod
    def validate_time_units(cls, v):
        """Validate time unit values."""
        if v not in cls.VALID_TIME_UNITS:
            raise ValueError(f"Time unit must be one of: {', '.join(cls.VALID_TIME_UNITS)}")
        return v
    
    @field_validator('notification_wanted')
    @classmethod
    def validate_notification_wanted(cls, v):
        """Validate notification wanted field."""
        if v not in ["Y", "N"]:
            raise ValueError("Notification wanted must be 'Y' or 'N'")
        return v
    
    @field_validator('duedate')
    @classmethod
    def validate_duedate(cls, v):
        """Validate due date is in the future."""
        if v is not None:
            # Handle timezone-aware datetime comparison
            now = datetime.now()
            if v.tzinfo is not None:
                # If v is timezone-aware, make now timezone-aware too
                from datetime import timezone
                now = now.replace(tzinfo=timezone.utc)
            if v <= now:
                raise ValueError("Due date must be in the future")
        return v


class TaskHistoryEntry(BaseModel):
    """Task history entry for tracking status changes."""
    
    previous_status: str = Field(...)
    new_status: str = Field(...)
    lastmoddate: datetime = Field(default_factory=datetime.now)
    reason: str = Field(default="")
    
    @field_validator('previous_status', 'new_status')
    @classmethod
    def validate_status(cls, v):
        """Validate status values."""
        valid_statuses = ["Created", "Started", "InProcess", "Modified", "Scheduled", "Complete", "Deleted"]
        if v not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return v


class BeanieTask(Document):
    """Task document model using Beanie ODM."""
    
    VALID_STATUSES: ClassVar[List[str]] = ["Created", "Started", "InProcess", "Modified", "Scheduled", "Complete", "Deleted"]
    
    # Required fields
    user: Link[BeanieUser] = Field(..., description="User who owns this task")
    title: str = Field(..., min_length=1, max_length=50)
    
    # Optional fields
    description: str = Field(default="", max_length=250)
    labels: List[Label] = Field(default_factory=list)
    task_mgmt: Optional[TaskMgmtDetails] = Field(None)
    task_history: List[TaskHistoryEntry] = Field(default_factory=list)
    status: str = Field(default="Created")
    
    # Timestamps
    createdate: datetime = Field(default_factory=datetime.now)
    lastmoddate: datetime = Field(default_factory=datetime.now)
    
    class Settings:
        name = "tasks"  # Collection name
        indexes = [
            IndexModel([("user", 1)]),
            IndexModel([("status", 1)]),
            IndexModel([("createdate", -1)]),
            IndexModel([("lastmoddate", -1)]),
            IndexModel([("task_mgmt.priority", 1)]),
            IndexModel([("task_mgmt.duedate", 1)]),
            IndexModel([("labels.name", 1)]),
        ]
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        """Validate title field."""
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        """Validate description field."""
        return v.strip() if v else ""
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        """Validate status field."""
        if v not in cls.VALID_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(cls.VALID_STATUSES)}")
        return v
    
    def update_status(self, new_status: str, reason: str = "") -> None:
        """Update task status and add entry to history."""
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(self.VALID_STATUSES)}")
        
        # Add history entry
        history_entry = TaskHistoryEntry(
            previous_status=self.status,
            new_status=new_status,
            reason=reason
        )
        self.task_history = self.task_history + [history_entry]
        
        # Update status and modification date
        self.status = new_status
        self.lastmoddate = datetime.now()
    
    def to_response(self) -> dict:
        """Convert task to API response format."""
        return {
            "id": str(self.id),
            "user_id": str(self.user.id) if hasattr(self.user, 'id') else None,
            "title": self.title,
            "description": self.description,
            "labels": [{"name": label.name, "color": label.color} for label in self.labels],
            "task_mgmt": self.task_mgmt.dict() if self.task_mgmt is not None else None,  # type: ignore[attr-defined]
            "status": self.status,
            "createdate": self.createdate,
            "lastmoddate": self.lastmoddate
        }
    
    def __str__(self) -> str:
        """String representation of Task."""
        priority_str = f"P{self.task_mgmt.priority}" if self.task_mgmt is not None else "No Priority"  # type: ignore[attr-defined]
        return f"Task({self.title} - {priority_str} - {self.status})"
    
    def __repr__(self) -> str:
        """Debug representation of Task."""
        return self.__str__()
