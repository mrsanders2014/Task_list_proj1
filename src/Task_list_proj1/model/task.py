"""
Task Model
Defines the Task data structure and validation.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from bson import ObjectId


class Label:
    """Label model for task categorization."""
    
    def __init__(self, name: str, color: str = "#808080"):
        """
        Initialize a Label instance.
        
        Args:
            name: Label name
            color: Label color in hex format
        """
        self.name = name
        self.color = color
    
    def to_dict(self) -> Dict[str, str]:
        """Convert Label to dictionary."""
        return {"name": self.name, "color": self.color}
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Label':
        """Create Label from dictionary."""
        return cls(name=data.get('name', ''), color=data.get('color', '#808080'))
    
    def __str__(self) -> str:
        return f"{self.name} ({self.color})"


class Task:
    """Task model representing a task in the system."""
    
    VALID_STATUSES = ["open", "inprocess", "completed", "deleted"]
    VALID_TIME_UNITS = ["minutes", "hours", "days", "weeks"]
    VALID_NOTIFICATION_UNITS = ["minutes", "hours", "days", "weeks"]
    
    def __init__(
        self,
        user_id: str,
        title: str,
        description: str = "",
        priority: Optional[int] = None,
        due_date: Optional[datetime] = None,
        labels: Optional[List[Label]] = None,
        time_unit: str = "hours",
        estimated_time: Optional[float] = None,
        status: str = "open",
        notification_time_unit: str = "hours",
        notification_when: Optional[float] = None,
        dependencies: Optional[List[str]] = None,
        _id: Optional[ObjectId] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        """
        Initialize a Task instance.
        
        Args:
            user_id: ID of the user who owns this task
            title: Task title
            description: Task description
            priority: Priority level (1-10, optional)
            due_date: Due date for the task (optional)
            labels: List of labels for categorization
            time_unit: Unit of time for estimation (minutes, hours, days, weeks)
            estimated_time: Estimated number of time units to complete
            status: Task status (open, inprocess, completed, deleted)
            notification_time_unit: Unit for notification timing
            notification_when: When to send notification (in notification_time_unit before due_date)
            dependencies: List of task IDs that this task depends on
            _id: MongoDB ObjectId
            created_at: Timestamp when task was created
            updated_at: Timestamp when task was last updated
        """
        self._id = _id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.labels = labels or []
        self.time_unit = time_unit
        self.estimated_time = estimated_time
        self.status = status
        self.notification_time_unit = notification_time_unit
        self.notification_when = notification_when
        self.dependencies = dependencies or []
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        
        self._validate()
    
    def _validate(self) -> None:
        """Validate task data."""
        if not self.user_id or not self.user_id.strip():
            raise ValueError("User ID is required")
        
        if not self.title or not self.title.strip():
            raise ValueError("Title is required")
        
        if self.priority is not None:
            if not isinstance(self.priority, int) or not 1 <= self.priority <= 10:
                raise ValueError("Priority must be an integer between 1 and 10")
        
        if self.status not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(self.VALID_STATUSES)}")
        
        if self.time_unit not in self.VALID_TIME_UNITS:
            raise ValueError(f"Time unit must be one of: {', '.join(self.VALID_TIME_UNITS)}")
        
        if self.notification_time_unit not in self.VALID_NOTIFICATION_UNITS:
            raise ValueError(f"Notification time unit must be one of: {', '.join(self.VALID_NOTIFICATION_UNITS)}")
        
        if self.estimated_time is not None and self.estimated_time < 0:
            raise ValueError("Estimated time must be a positive number")
        
        if self.notification_when is not None and self.notification_when < 0:
            raise ValueError("Notification time must be a positive number")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert Task instance to dictionary for MongoDB storage.
        
        Returns:
            Dict containing task data
        """
        data = {
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date,
            "labels": [label.to_dict() for label in self.labels],
            "time_unit": self.time_unit,
            "estimated_time": self.estimated_time,
            "status": self.status,
            "notification_time_unit": self.notification_time_unit,
            "notification_when": self.notification_when,
            "dependencies": self.dependencies,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        
        if self._id is not None:
            data["_id"] = self._id
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """
        Create Task instance from dictionary.
        
        Args:
            data: Dictionary containing task data
            
        Returns:
            Task instance
        """
        labels_data = data.get('labels', [])
        labels = [Label.from_dict(label) for label in labels_data] if labels_data else []
        
        return cls(
            user_id=data.get('user_id', ''),
            title=data.get('title', ''),
            description=data.get('description', ''),
            priority=data.get('priority'),
            due_date=data.get('due_date'),
            labels=labels,
            time_unit=data.get('time_unit', 'hours'),
            estimated_time=data.get('estimated_time'),
            status=data.get('status', 'open'),
            notification_time_unit=data.get('notification_time_unit', 'hours'),
            notification_when=data.get('notification_when'),
            dependencies=data.get('dependencies', []),
            _id=data.get('_id'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def __str__(self) -> str:
        """String representation of Task."""
        priority_str = f"P{self.priority}" if self.priority else "No Priority"
        return f"Task({self.title} - {priority_str} - {self.status})"
    
    def __repr__(self) -> str:
        """Debug representation of Task."""
        return self.__str__()

