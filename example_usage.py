"""
Example usage of the Task Management system
This script demonstrates how to use the Task model and repository programmatically
"""

from datetime import datetime, timedelta
from src.Task_list_proj1.model.Task_class import Task
from src.Task_list_proj1.dbase.task_repository import TaskRepository


def main():
    """Demonstrate Task Management system usage"""
    
    print("=" * 60)
    print("Task Management System - Example Usage")
    print("=" * 60)
    
    # Initialize repository
    print("\n1. Initializing repository...")
    repo = TaskRepository()
    print("✓ Repository initialized")
    
    # Create sample tasks
    print("\n2. Creating sample tasks...")
    
    task1 = Task(
        title="Complete project documentation",
        description="Write comprehensive README and setup guides",
        priority="High",
        status="In Progress",
        due_date=datetime.now() + timedelta(days=7),
        user="Michael Sanders"
    )
    
    task2 = Task(
        title="Implement user authentication",
        description="Add JWT-based authentication to the API",
        priority="High",
        status="Pending",
        due_date=datetime.now() + timedelta(days=14),
        predecessor_task=None
    )
    
    task3 = Task(
        title="Design database schema",
        description="Create ERD and define collections",
        priority="Medium",
        status="Completed",
        due_date=datetime.now() - timedelta(days=3),
        color="green"
    )
    
    # Insert tasks
    id1 = repo.create(task1)
    id2 = repo.create(task2)
    id3 = repo.create(task3)
    
    print(f"✓ Created task 1: {id1}")
    print(f"✓ Created task 2: {id2}")
    print(f"✓ Created task 3: {id3}")
    
    # Read all tasks
    print("\n3. Reading all tasks...")
    all_tasks = repo.read_all()
    print(f"✓ Found {len(all_tasks)} tasks")
    for task in all_tasks:
        print(f"   - {task.title} [{task.status}]")
    
    # Read specific task
    print(f"\n4. Reading task by ID: {id1}")
    task = repo.read(id1)
    if task:
        print(f"✓ Found task: {task.title}")
        print(f"   Priority: {task.priority}")
        print(f"   Status: {task.status}")
        print(f"   Due: {task.due_date.strftime('%Y-%m-%d') if task.due_date else 'N/A'}")
    
    # Update task
    print(f"\n5. Updating task {id1}...")
    update_data = {
        "status": "Completed",
        "updated_at": datetime.now()
    }
    success = repo.update(id1, update_data)
    if success:
        print("✓ Task updated successfully")
        updated_task = repo.read(id1)
        print(f"   New status: {updated_task.status}")
    
    # Search tasks
    print("\n6. Searching for tasks containing 'documentation'...")
    search_results = repo.search("documentation", "title")
    print(f"✓ Found {len(search_results)} task(s)")
    for task in search_results:
        print(f"   - {task.title}")
    
    # Filter by status
    print("\n7. Filtering tasks by status 'Completed'...")
    completed_tasks = repo.get_by_status("Completed")
    print(f"✓ Found {len(completed_tasks)} completed task(s)")
    for task in completed_tasks:
        print(f"   - {task.title}")
    
    # Filter by priority
    print("\n8. Filtering tasks by priority 'High'...")
    high_priority = repo.get_by_priority("High")
    print(f"✓ Found {len(high_priority)} high priority task(s)")
    for task in high_priority:
        print(f"   - {task.title}")
    
    # Delete specific task
    print(f"\n9. Deleting task {id3}...")
    deleted = repo.delete(id3)
    if deleted:
        print("✓ Task deleted successfully")
    
    # Count remaining tasks
    remaining = repo.read_all()
    print(f"\n10. Remaining tasks: {len(remaining)}")
    
    # Clean up - delete all test tasks
    print("\n11. Cleaning up test data...")
    count = repo.delete_all()
    print(f"✓ Deleted {count} task(s)")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)
    
    # Close connection
    repo.client.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure:")
        print("  1. MongoDB is running")
        print("  2. .env file is configured")
        print("  3. Dependencies are installed (uv sync)")

