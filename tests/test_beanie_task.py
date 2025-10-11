"""
Unit tests for Beanie Task model.
"""
# pylint: disable=no-member
from datetime import datetime

import pytest

from src.models.beanie_task import BeanieTask, Label, TaskMgmtDetails, TaskHistoryEntry
from src.models.beanie_user import BeanieUser


def test_label_creation():
    """Test creating a label."""
    label = Label(name="Work", color="#FF5733")
    
    assert label.name == "Work"
    assert label.color == "#FF5733"


def test_label_default_color():
    """Test label with default color."""
    label = Label(name="Personal")
    
    assert label.name == "Personal"
    assert label.color == "#808080"


def test_task_mgmt_details_creation():
    """Test creating task management details."""
    due_date = datetime(2025, 12, 31)
    task_mgmt = TaskMgmtDetails(
        priority=8,
        duedate=due_date,
        estimated_time_to_complete=2.5,
        time_unit="hours"
    )
    
    assert task_mgmt.priority == 8
    assert task_mgmt.duedate == due_date
    assert task_mgmt.estimated_time_to_complete == 2.5
    assert task_mgmt.time_unit == "hours"
    assert task_mgmt.notify_time == 0
    assert task_mgmt.notification_wanted == "N"


def test_task_mgmt_validation_invalid_priority():
    """Test task management validation fails with invalid priority."""
    with pytest.raises(ValueError, match="Priority must be an integer between 1 and 10"):
        TaskMgmtDetails(priority=15)


def test_task_mgmt_validation_invalid_time_unit():
    """Test task management validation fails with invalid time unit."""
    with pytest.raises(ValueError, match="Time unit must be one of"):
        TaskMgmtDetails(time_unit="invalid_unit")


def test_task_mgmt_validation_invalid_notification():
    """Test task management validation fails with invalid notification."""
    with pytest.raises(ValueError, match="Notification wanted must be 'Y' or 'N'"):
        TaskMgmtDetails(notification_wanted="Maybe")


def test_task_history_entry_creation():
    """Test creating task history entry."""
    history = TaskHistoryEntry(
        previous_status="Created",
        new_status="InProcess",
        reason="Started working on task"
    )
    
    assert history.previous_status == "Created"
    assert history.new_status == "InProcess"
    assert history.reason == "Started working on task"
    assert isinstance(history.lastmoddate, datetime)


def test_task_history_validation_invalid_status():
    """Test task history validation fails with invalid status."""
    with pytest.raises(ValueError, match="Status must be one of"):
        TaskHistoryEntry(
            previous_status="InvalidStatus",
            new_status="Created"
        )


def test_beanie_task_creation():
    """Test creating a valid BeanieTask."""
    user = BeanieUser(username="testuser", email="test@example.com")
    task_mgmt = TaskMgmtDetails(priority=8)
    
    task = BeanieTask(
        user=user,
        title="Complete project",
        description="Finish the task management system",
        task_mgmt=task_mgmt,
        status="Created"
    )
    
    assert task.user == user
    assert task.title == "Complete project"
    assert task.description == "Finish the task management system"
    assert task.task_mgmt.priority == 8  # type: ignore[attr-defined]
    assert task.status == "Created"
    assert isinstance(task.createdate, datetime)
    assert isinstance(task.lastmoddate, datetime)


def test_beanie_task_validation_missing_title():
    """Test task validation fails with missing title."""
    user = BeanieUser(username="testuser", email="test@example.com")
    
    with pytest.raises(ValueError, match="Title cannot be empty"):
        BeanieTask(
            user=user,
            title=""
        )


def test_beanie_task_validation_invalid_status():
    """Test task validation fails with invalid status."""
    user = BeanieUser(username="testuser", email="test@example.com")
    
    with pytest.raises(ValueError, match="Status must be one of"):
        BeanieTask(
            user=user,
            title="Test Task",
            status="invalid_status"
        )


def test_beanie_task_with_labels():
    """Test creating task with labels."""
    user = BeanieUser(username="testuser", email="test@example.com")
    labels = [
        Label(name="Work", color="#FF5733"),
        Label(name="Urgent", color="#FFC300")
    ]
    
    task = BeanieTask(
        user=user,
        title="Important Task",
        labels=labels
    )
    
    assert len(task.labels) == 2
    assert task.labels[0].name == "Work"
    assert task.labels[1].name == "Urgent"


def test_beanie_task_update_status():
    """Test updating task status."""
    user = BeanieUser(username="testuser", email="test@example.com")
    task = BeanieTask(
        user=user,
        title="Test Task",
        status="Created"
    )
    
    initial_lastmoddate = task.lastmoddate
    task.update_status("InProcess", "Started working on task")
    
    assert task.status == "InProcess"
    assert task.lastmoddate != initial_lastmoddate
    assert len(task.task_history) == 1
    assert task.task_history[0].previous_status == "Created"
    assert task.task_history[0].new_status == "InProcess"
    assert task.task_history[0].reason == "Started working on task"


def test_beanie_task_update_status_invalid():
    """Test updating task status with invalid status."""
    user = BeanieUser(username="testuser", email="test@example.com")
    task = BeanieTask(
        user=user,
        title="Test Task",
        status="Created"
    )
    
    with pytest.raises(ValueError, match="Status must be one of"):
        task.update_status("InvalidStatus")


def test_beanie_task_to_response():
    """Test converting task to response format."""
    user = BeanieUser(username="testuser", email="test@example.com")
    task_mgmt = TaskMgmtDetails(priority=5)
    task = BeanieTask(
        user=user,
        title="Test Task",
        description="Test description",
        task_mgmt=task_mgmt
    )
    
    response = task.to_response()
    
    assert "id" in response
    assert response["title"] == "Test Task"
    assert response["description"] == "Test description"
    assert response["status"] == "Created"
    assert "createdate" in response
    assert "lastmoddate" in response
    assert response["task_mgmt"] is not None


def test_beanie_task_str_representation():
    """Test string representation of task."""
    user = BeanieUser(username="testuser", email="test@example.com")
    task_mgmt = TaskMgmtDetails(priority=8)
    task = BeanieTask(
        user=user,
        title="Test Task",
        task_mgmt=task_mgmt,
        status="Created"
    )
    
    task_str = str(task)
    assert "Test Task" in task_str
    assert "P8" in task_str
    assert "Created" in task_str


def test_beanie_task_optional_fields():
    """Test task with optional fields."""
    user = BeanieUser(username="testuser", email="test@example.com")
    due_date = datetime(2025, 12, 31)
    
    task_mgmt = TaskMgmtDetails(
        priority=3,
        duedate=due_date,
        estimated_time_to_complete=5.5,
        notify_time=24.0
    )
    
    task = BeanieTask(
        user=user,
        title="Task with Options",
        task_mgmt=task_mgmt
    )
    
    assert task.task_mgmt.duedate == due_date
    assert abs(task.task_mgmt.estimated_time_to_complete - 5.5) < 0.001  # type: ignore[attr-defined]
    assert abs(task.task_mgmt.notify_time - 24.0) < 0.001  # type: ignore[attr-defined]
