"""
Unit tests for Task model.
"""
import pytest
from datetime import datetime
from src.Task_list_proj1.model.task import Task, Label


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
    task = Task(
        user_id="user123",
        title="Complete project",
        description="Finish the task management system",
        priority=8,
        status="open"
    )
    
    assert task.user_id == "user123"
    assert task.title == "Complete project"
    assert task.description == "Finish the task management system"
    assert task.priority == 8
    assert task.status == "open"
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)


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
        Task(
            user_id="user123",
            title="Test Task",
            priority=15
        )


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
        Task(
            user_id="user123",
            title="Test Task",
            time_unit="years"
        )


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


def test_task_with_dependencies():
    """Test creating task with dependencies."""
    dependencies = ["task_id_1", "task_id_2"]
    
    task = Task(
        user_id="user123",
        title="Dependent Task",
        dependencies=dependencies
    )
    
    assert len(task.dependencies) == 2
    assert "task_id_1" in task.dependencies
    assert "task_id_2" in task.dependencies


def test_task_to_dict():
    """Test converting task to dictionary."""
    task = Task(
        user_id="user123",
        title="Test Task",
        description="Test description",
        priority=5
    )
    
    task_dict = task.to_dict()
    
    assert task_dict["user_id"] == "user123"
    assert task_dict["title"] == "Test Task"
    assert task_dict["description"] == "Test description"
    assert task_dict["priority"] == 5
    assert task_dict["status"] == "open"
    assert "created_at" in task_dict
    assert "updated_at" in task_dict


def test_task_from_dict():
    """Test creating task from dictionary."""
    task_data = {
        "user_id": "user456",
        "title": "Another Task",
        "description": "Task from dict",
        "priority": 7,
        "status": "inprocess",
        "labels": [
            {"name": "Personal", "color": "#3498db"}
        ],
        "dependencies": ["task_xyz"]
    }
    
    task = Task.from_dict(task_data)
    
    assert task.user_id == "user456"
    assert task.title == "Another Task"
    assert task.priority == 7
    assert task.status == "inprocess"
    assert len(task.labels) == 1
    assert task.labels[0].name == "Personal"
    assert len(task.dependencies) == 1


def test_task_str_representation():
    """Test string representation of task."""
    task = Task(
        user_id="user123",
        title="Test Task",
        priority=8,
        status="open"
    )
    
    task_str = str(task)
    assert "Test Task" in task_str
    assert "P8" in task_str
    assert "open" in task_str


def test_task_optional_fields():
    """Test task with optional fields."""
    due_date = datetime(2025, 12, 31)
    
    task = Task(
        user_id="user123",
        title="Task with Options",
        due_date=due_date,
        estimated_time=5.5,
        notification_when=24.0
    )
    
    assert task.due_date == due_date
    assert task.estimated_time == 5.5
    assert task.notification_when == 24.0
