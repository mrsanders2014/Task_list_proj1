"""
Task Model
Defines the Task data structure and validation.
"""
from datetime import datetime, timedelta
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


class TaskTimeMgmt:
    """Task time management details."""
    
    def __init__(
        self,
        create_date: Optional[datetime] = None,
        scheduled_start_date: Optional[datetime] = None,
        actual_start_date: Optional[datetime] = None,
        scheduled_comp_date: Optional[datetime] = None,
        actual_comp_date: Optional[datetime] = None,
        archived_date: Optional[datetime] = None
    ):
        """
        Initialize a TaskTimeMgmt instance.
        
        Args:
            create_date: Timestamp when the task was created
            scheduled_start_date: Scheduled start date
            actual_start_date: Actual start date
            scheduled_comp_date: Scheduled completion date
            actual_comp_date: Actual completion date
            archived_date: Date when task was archived
        """
        self.create_date = create_date or datetime.now()
        self.scheduled_start_date = scheduled_start_date
        self.actual_start_date = actual_start_date
        self.scheduled_comp_date = scheduled_comp_date
        self.actual_comp_date = actual_comp_date
        self.archived_date = archived_date
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert TaskTimeMgmt to dictionary."""
        return {
            "create_date": self.create_date,
            "scheduled_start_date": self.scheduled_start_date,
            "actual_start_date": self.actual_start_date,
            "scheduled_comp_date": self.scheduled_comp_date,
            "actual_comp_date": self.actual_comp_date,
            "archived_date": self.archived_date
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskTimeMgmt':
        """Create TaskTimeMgmt from dictionary."""
        return cls(
            create_date=data.get('create_date'),
            scheduled_start_date=data.get('scheduled_start_date'),
            actual_start_date=data.get('actual_start_date'),
            scheduled_comp_date=data.get('scheduled_comp_date'),
            actual_comp_date=data.get('actual_comp_date'),
            archived_date=data.get('archived_date')
        )


class TaskMgmtDetails:
    """Task management details including priority, deadlines, and notifications."""
    
    VALID_TIME_UNITS = ["minutes", "hours", "days", "weeks", "months", "years"]
    
    def __init__(
        self,
        priority: int = 1,
        duedate: Optional[datetime] = None,
        time_unit: str = "hours",
        estimated_time_to_complete: Optional[float] = None,
        notify_time: float = 0,
        notify_time_units: str = "hours",
        notification_wanted: str = "N",
        time_mgmt: Optional[List[TaskTimeMgmt]] = None
    ):
        """
        Initialize a TaskMgmtDetails instance.
        
        Args:
            priority: Priority level (1-10, where 1 is high and 10 is low)
            duedate: Due date for the task (must be at least 1 minute in the future)
            time_unit: Unit of time for estimation
            estimated_time_to_complete: Estimated time in time_units (minimum 1)
            notify_time: Notification time before due date
            notify_time_units: Units for notification time
            notification_wanted: Whether notifications are wanted (Y/N)
            time_mgmt: List of time management records
        """
        self.priority = priority
        self.duedate = duedate
        self.time_unit = time_unit
        self.estimated_time_to_complete = estimated_time_to_complete
        self.notify_time = notify_time
        self.notify_time_units = notify_time_units
        self.notification_wanted = notification_wanted
        self.time_mgmt = time_mgmt or []
        
        self._validate()
    
    def _validate(self) -> None:
        """Validate task management details."""
        if not isinstance(self.priority, int) or not 1 <= self.priority <= 10:
            raise ValueError("Priority must be an integer between 1 and 10")
        
        if self.duedate is not None:
            if not isinstance(self.duedate, datetime):
                raise ValueError("Due date must be a datetime object")
            # Check if due date is at least 1 minute in the future
            if self.duedate <= datetime.now() + timedelta(minutes=1):
                raise ValueError("Due date must be at least 1 minute in the future from creation time")
        
        if self.time_unit not in self.VALID_TIME_UNITS:
            raise ValueError(f"Time unit must be one of: {', '.join(self.VALID_TIME_UNITS)}")
        
        if self.estimated_time_to_complete is not None:
            if not isinstance(self.estimated_time_to_complete, (int, float)) or self.estimated_time_to_complete < 1:
                raise ValueError("Estimated time to complete must be at least 1 time_unit")
        
        if self.notify_time_units not in self.VALID_TIME_UNITS:
            raise ValueError(f"Notify time units must be one of: {', '.join(self.VALID_TIME_UNITS)}")
        
        if self.notification_wanted not in ["Y", "N"]:
            raise ValueError("Notification wanted must be 'Y' or 'N'")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert TaskMgmtDetails to dictionary."""
        return {
            "priority": self.priority,
            "duedate": self.duedate,
            "time_unit": self.time_unit,
            "estimated_time_to_complete": self.estimated_time_to_complete,
            "notify_time": self.notify_time,
            "notify_time_units": self.notify_time_units,
            "notification_wanted": self.notification_wanted,
            "time_mgmt": [tm.to_dict() for tm in self.time_mgmt]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskMgmtDetails':
        """Create TaskMgmtDetails from dictionary."""
        time_mgmt_data = data.get('time_mgmt', [])
        time_mgmt = [TaskTimeMgmt.from_dict(tm) for tm in time_mgmt_data] if time_mgmt_data else []
        
        return cls(
            priority=data.get('priority', 1),
            duedate=data.get('duedate'),
            time_unit=data.get('time_unit', 'hours'),
            estimated_time_to_complete=data.get('estimated_time_to_complete'),
            notify_time=data.get('notify_time', 0),
            notify_time_units=data.get('notify_time_units', 'hours'),
            notification_wanted=data.get('notification_wanted', 'N'),
            time_mgmt=time_mgmt
        )


class TaskHistoryEntry:
    """Task history entry for tracking status changes."""
    
    def __init__(
        self,
        previous_status: str,
        new_status: str,
        lastmoddate: datetime,
        reason: str = ""
    ):
        """
        Initialize a TaskHistoryEntry instance.
        
        Args:
            previous_status: Previous status
            new_status: New status
            lastmoddate: Date of modification
            reason: Reason for status change
        """
        self.previous_status = previous_status
        self.new_status = new_status
        self.lastmoddate = lastmoddate
        self.reason = reason
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert TaskHistoryEntry to dictionary."""
        return {
            "previous_status": self.previous_status,
            "new_status": self.new_status,
            "lastmoddate": self.lastmoddate,
            "reason": self.reason
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskHistoryEntry':
        """Create TaskHistoryEntry from dictionary."""
        return cls(
            previous_status=data.get('previous_status', ''),
            new_status=data.get('new_status', ''),
            lastmoddate=data.get('lastmoddate', datetime.now()),
            reason=data.get('reason', '')
        )


class Task:
    """Task model representing a task in the system."""
    
    VALID_STATUSES = ["Created", "Started", "InProcess", "Modified", "Scheduled", "Complete", "Deleted"]
    
    def __init__(
        self,
        user_id: str,
        title: str,
        description: str = "",
        labels: Optional[List[Label]] = None,
        task_mgmt: Optional[TaskMgmtDetails] = None,
        task_history: Optional[List[TaskHistoryEntry]] = None,
        status: str = "Created",
        _id: Optional[ObjectId] = None,
        createdate: Optional[datetime] = None,
        lastmoddate: Optional[datetime] = None
    ):
        """
        Initialize a Task instance.
        
        Args:
            user_id: MongoDB ID of the user who owns this task
            title: Task title (max 50 characters, required)
            description: Task description (max 250 characters, optional)
            labels: Optional list of labels for categorization
            task_mgmt: Optional task management details
            task_history: List of status change history entries
            status: Task status (Created, Started, InProcess, Modified, Scheduled, Complete, Deleted)
            _id: MongoDB ObjectId assigned by database
            createdate: Timestamp when task was created
            lastmoddate: Timestamp when task was last modified
        """
        self._id = _id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.labels = labels or []
        self.task_mgmt = task_mgmt
        self.task_history = task_history or []
        self.status = status
        self.createdate = createdate or datetime.now()
        self.lastmoddate = lastmoddate or datetime.now()
        
        self._validate()
    
    def _validate(self) -> None:
        """Validate task data."""
        if not self.user_id or not self.user_id.strip():
            raise ValueError("User ID is required")
        
        if not self.title or not self.title.strip():
            raise ValueError("Title is required")
        
        if len(self.title) > 50:
            raise ValueError("Title must be 50 characters or less")
        
        if len(self.description) > 250:
            raise ValueError("Description must be 250 characters or less")
        
        if self.status not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(self.VALID_STATUSES)}")
    
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
            "createdate": self.createdate,
            "lastmoddate": self.lastmoddate,
            "status": self.status,
            "labels": [label.to_dict() for label in self.labels] if self.labels else [],
            "task_mgmt": self.task_mgmt.to_dict() if self.task_mgmt else None,
            "task_history": [entry.to_dict() for entry in self.task_history] if self.task_history else []
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
        
        task_mgmt_data = data.get('task_mgmt')
        task_mgmt = TaskMgmtDetails.from_dict(task_mgmt_data) if task_mgmt_data else None
        
        task_history_data = data.get('task_history', [])
        task_history = [TaskHistoryEntry.from_dict(entry) for entry in task_history_data] if task_history_data else []
        
        return cls(
            user_id=data.get('user_id', ''),
            title=data.get('title', ''),
            description=data.get('description', ''),
            labels=labels,
            task_mgmt=task_mgmt,
            task_history=task_history,
            status=data.get('status', 'Created'),
            _id=data.get('_id'),
            createdate=data.get('createdate'),
            lastmoddate=data.get('lastmoddate')
        )
    
    def update_status(self, new_status: str, reason: str = "") -> None:
        """
        Update task status and add entry to history.
        
        Args:
            new_status: New status to set
            reason: Reason for status change
        """
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(self.VALID_STATUSES)}")
        
        # Add history entry
        history_entry = TaskHistoryEntry(
            previous_status=self.status,
            new_status=new_status,
            lastmoddate=datetime.now(),
            reason=reason
        )
        self.task_history.append(history_entry)
        
        # Update status and modification date
        self.status = new_status
        self.lastmoddate = datetime.now()
    
    def __str__(self) -> str:
        """String representation of Task."""
        priority_str = f"P{self.task_mgmt.priority}" if self.task_mgmt else "No Priority"
        return f"Task({self.title} - {priority_str} - {self.status})"
    
    def __repr__(self) -> str:
        """Debug representation of Task."""
        return self.__str__()

