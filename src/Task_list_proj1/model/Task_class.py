"""
Task model for the Task TODO application
"""

from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from bson import ObjectId


@dataclass
class Task:
    """Task entity model"""
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "Medium"  # High, Medium, Low
    status: str = "Pending"  # Pending, In Progress, Completed, Deleted
    due_date: Optional[datetime] = None
    color: Optional[str] = None
    time_unit: Optional[str] = None
    can_parallel: bool = False
    parallel_tasks: Optional[list] = None
    predecessor_task: Optional[str] = None
    user: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now
    _id: Optional[ObjectId] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for database storage"""
        data = {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "due_date": self.due_date,
            "color": self.color,
            "time_unit": self.time_unit,
            "can_parallel": self.can_parallel,
            "parallel_tasks": self.parallel_tasks,
            "predecessor_task": self.predecessor_task,
            "user": self.user,
            "created_at": self.created_at
        }
        
        if self.updated_at:
            data["updated_at"] = self.updated_at
            
        if self._id:
            data["_id"] = self._id
            
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create Task instance from dictionary (e.g., from database)"""
        return cls(
            title=data.get("title", ""),
            description=data.get("description"),
            priority=data.get("priority", "Medium"),
            status=data.get("status", "Pending"),
            due_date=data.get("due_date"),
            color=data.get("color"),
            time_unit=data.get("time_unit"),
            can_parallel=data.get("can_parallel", False),
            parallel_tasks=data.get("parallel_tasks"),
            predecessor_task=data.get("predecessor_task"),
            user=data.get("user"),
            created_at=data.get("created_at", datetime.now()),
            updated_at=data.get("updated_at"),
            _id=data.get("_id")
        )
    
    def update(self, **kwargs) -> None:
        """Update task fields and set updated_at timestamp"""
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ('_id', 'created_at'):
                setattr(self, key, value)
        self.updated_at = datetime.now()
    
    def __str__(self) -> str:
        """String representation of the task"""
        status_str = f"[{self.status}]"
        priority_str = f"Priority: {self.priority}"
        due_str = f" | Due: {self.due_date.strftime('%Y-%m-%d')}" if self.due_date else ""
        return f"{status_str} {self.title} - {priority_str}{due_str}"
    
    def __repr__(self) -> str:
        """Detailed representation of the task"""
        return (f"Task(title='{self.title}', status='{self.status}', "
                f"priority='{self.priority}', due_date={self.due_date})")
    
    def to_response(self) -> Dict[str, Any]:
        """Convert task to API response format"""
        return {
            "id": str(self._id) if self._id else None,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "due_date": self.due_date,
            "color": self.color,
            "time_unit": self.time_unit,
            "can_parallel": self.can_parallel,
            "parallel_tasks": self.parallel_tasks,
            "predecessor_task": self.predecessor_task,
            "user": self.user,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }