"""
Unit tests for Task model.
"""
from datetime import datetime

import pytest

from src.model.task import Task, Label, TaskMgmtDetails


def test_label_creation():
    """Test creating a label."""
    label = Label("Work", "#FF5733")
    
    assert label.name == "Work"
    assert label.color == "#FF5733"


def test_label_default_color():
    """Test label with default color."""
    label = Label("Personal")
    
    assert label.name == "Personal"
    assert label.color == "#808080"


def test_task_creation():
    """Test creating a valid task."""
    task_mgmt = TaskMgmtDetails(priority=8)
    task = Task(
        user_id="user123",
        title="Complete project",
        description="Finish the task management system",
        task_mgmt=task_mgmt,
        status="Created"
    )
    
    assert task.user_id == "user123"
    assert task.title == "Complete project"
    assert task.description == "Finish the task management system"
    assert task.task_mgmt.priority == 8
    assert task.status == "Created"
    assert isinstance(task.createdate, datetime)
    assert isinstance(task.lastmoddate, datetime)


def test_task_validation_missing_user_id():
    """Test task validation fails with missing user_id."""
    with pytest.raises(ValueError, match="User ID is required"):
        Task(
            user_id="",
            title="Test Task"
        )


def test_task_validation_missing_title():
    """Test task validation fails with missing title."""
    with pytest.raises(ValueError, match="Title is required"):
        Task(
            user_id="user123",
            title=""
        )


def test_task_validation_invalid_priority():
    """Test task validation fails with invalid priority."""
    with pytest.raises(ValueError, match="Priority must be an integer between 1 and 10"):
        TaskMgmtDetails(priority=15)


def test_task_validation_invalid_status():
    """Test task validation fails with invalid status."""
    with pytest.raises(ValueError, match="Status must be one of"):
        Task(
            user_id="user123",
            title="Test Task",
            status="invalid_status"
        )


def test_task_validation_invalid_time_unit():
    """Test task validation fails with invalid time unit."""
    with pytest.raises(ValueError, match="Time unit must be one of"):
        TaskMgmtDetails(time_unit="invalid_unit")


def test_task_with_labels():
    """Test creating task with labels."""
    labels = [
        Label("Work", "#FF5733"),
        Label("Urgent", "#FFC300")
    ]
    
    task = Task(
        user_id="user123",
        title="Important Task",
        labels=labels
    )
    
    assert len(task.labels) == 2
    assert task.labels[0].name == "Work"
    assert task.labels[1].name == "Urgent"


def test_task_with_task_mgmt():
    """Test creating task with task management details."""
    due_date = datetime(2025, 12, 31)
    task_mgmt = TaskMgmtDetails(
        priority=5,
        duedate=due_date,
        estimated_time_to_complete=2.5
    )
    
    task = Task(
        user_id="user123",
        title="Task with Management",
        task_mgmt=task_mgmt
    )
    
    assert task.task_mgmt.priority == 5
    assert task.task_mgmt.duedate == due_date
    assert abs(task.task_mgmt.estimated_time_to_complete - 2.5) < 0.001


def test_task_to_dict():
    """Test converting task to dictionary."""
    task_mgmt = TaskMgmtDetails(priority=5)
    task = Task(
        user_id="user123",
        title="Test Task",
        description="Test description",
        task_mgmt=task_mgmt
    )
    
    task_dict = task.to_dict()
    
    assert task_dict["user_id"] == "user123"
    assert task_dict["title"] == "Test Task"
    assert task_dict["description"] == "Test description"
    assert task_dict["task_mgmt"] is not None
    assert task_dict["status"] == "Created"
    assert "createdate" in task_dict
    assert "lastmoddate" in task_dict
    # Verify priority through the task object
    assert task.task_mgmt.priority == 5


def test_task_from_dict():
    """Test creating task from dictionary."""
    task_data = {
        "user_id": "user456",
        "title": "Another Task",
        "description": "Task from dict",
        "task_mgmt": {
            "priority": 7,
            "duedate": None,
            "time_unit": "hours",
            "estimated_time_to_complete": None,
            "notify_time": 0,
            "notify_time_units": "hours",
            "notification_wanted": "N",
            "time_mgmt": []
        },
        "status": "InProcess",
        "labels": [
            {"name": "Personal", "color": "#3498db"}
        ],
        "task_history": []
    }
    
    task = Task.from_dict(task_data)
    
    assert task.user_id == "user456"
    assert task.title == "Another Task"
    assert task.task_mgmt.priority == 7
    assert task.status == "InProcess"
    assert len(task.labels) == 1
    assert task.labels[0].name == "Personal"


def test_task_str_representation():
    """Test string representation of task."""
    task_mgmt = TaskMgmtDetails(priority=8)
    task = Task(
        user_id="user123",
        title="Test Task",
        task_mgmt=task_mgmt,
        status="Created"
    )
    
    task_str = str(task)
    assert "Test Task" in task_str
    assert "P8" in task_str
    assert "Created" in task_str


def test_task_optional_fields():
    """Test task with optional fields."""
    due_date = datetime(2025, 12, 31)
    
    task_mgmt = TaskMgmtDetails(
        priority=3,
        duedate=due_date,
        estimated_time_to_complete=5.5,
        notify_time=24.0
    )
    
    task = Task(
        user_id="user123",
        title="Task with Options",
        task_mgmt=task_mgmt
    )
    
    assert task.task_mgmt.duedate == due_date
    assert abs(task.task_mgmt.estimated_time_to_complete - 5.5) < 0.001
    assert abs(task.task_mgmt.notify_time - 24.0) < 0.001
