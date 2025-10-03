"""
Unit tests for Task model
"""

from datetime import datetime
import pytest
from src.Task_list_proj1.model.Task_class import Task


def test_task_creation():
    """Test basic task creation"""
    task = Task(
        title="Test Task",
        description="Test Description",
        priority="High",
        status="Pending"
    )
    
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.priority == "High"
    assert task.status == "Pending"
    assert task.created_at is not None


def test_task_defaults():
    """Test task default values"""
    task = Task(title="Simple Task")
    
    assert task.title == "Simple Task"
    assert task.priority == "Medium"
    assert task.status == "Pending"
    assert task.description is None
    assert task.can_parallel is False


def test_task_to_dict():
    """Test task conversion to dictionary"""
    task = Task(
        title="Test Task",
        priority="High",
        status="Completed"
    )
    
    task_dict = task.to_dict()
    
    assert task_dict["title"] == "Test Task"
    assert task_dict["priority"] == "High"
    assert task_dict["status"] == "Completed"
    assert "created_at" in task_dict


def test_task_from_dict():
    """Test task creation from dictionary"""
    data = {
        "title": "Test Task",
        "description": "Test Description",
        "priority": "Low",
        "status": "In Progress",
        "created_at": datetime.now()
    }
    
    task = Task.from_dict(data)
    
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.priority == "Low"
    assert task.status == "In Progress"


def test_task_update():
    """Test task update functionality"""
    task = Task(title="Original Title", status="Pending")
    
    assert task.updated_at is None
    
    task.update(title="Updated Title", status="Completed")
    
    assert task.title == "Updated Title"
    assert task.status == "Completed"
    assert task.updated_at is not None


def test_task_str_representation():
    """Test task string representation"""
    task = Task(
        title="Test Task",
        priority="High",
        status="Pending"
    )
    
    task_str = str(task)
    
    assert "Test Task" in task_str
    assert "Pending" in task_str
    assert "High" in task_str


def test_task_with_due_date():
    """Test task with due date"""
    due_date = datetime(2025, 12, 31)
    task = Task(
        title="Year End Task",
        due_date=due_date
    )
    
    assert task.due_date == due_date
    task_str = str(task)
    assert "2025-12-31" in task_str


def test_task_parallel_tasks():
    """Test task with parallel tasks"""
    task = Task(
        title="Parallel Task",
        can_parallel=True,
        parallel_tasks=["task1", "task2", "task3"]
    )
    
    assert task.can_parallel is True
    assert len(task.parallel_tasks) == 3
    assert "task1" in task.parallel_tasks


def test_task_to_response():
    """Test task response format"""
    task = Task(
        title="API Task",
        description="API Description",
        priority="Medium"
    )
    
    response = task.to_response()
    
    assert "title" in response
    assert "description" in response
    assert "priority" in response
    assert "id" in response
    assert response["title"] == "API Task"

