"""
Task Repository
Handles CRUD operations for Tasks collection.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId
from pymongo.errors import PyMongoError

from ..model.task import Task
from .connection import get_db_connection


class TaskRepository:
    """Repository for Task CRUD operations."""
    
    def __init__(self):
        """Initialize TaskRepository with database connection."""
        self.db_connection = get_db_connection()
        self.collection = self.db_connection.get_collection('Tasks')
    
    def create(self, task: Task) -> str:
        """
        Create a new task in the database.
        
        Args:
            task: Task instance to create
            
        Returns:
            str: ID of the created task
        """
        try:
            task_dict = task.to_dict()
            result = self.collection.insert_one(task_dict)
            return str(result.inserted_id)
        except PyMongoError as e:
            print(f"Error creating task: {e}")
            raise
    
    def get_by_id(self, object_id: str) -> Optional[Task]:
        """
        Retrieve a task by MongoDB ObjectId.
        
        Args:
            object_id: MongoDB ObjectId as string
            
        Returns:
            Task instance or None if not found
        """
        try:
            task_data = self.collection.find_one({"_id": ObjectId(object_id)})
            if task_data:
                return Task.from_dict(task_data)
            return None
        except Exception as e:
            print(f"Error retrieving task by ID: {e}")
            return None
    
    def get_by_user(self, user_id: str, status: Optional[str] = None) -> List[Task]:
        """
        Retrieve all tasks for a specific user.
        
        Args:
            user_id: User's unique identifier
            status: Optional filter by task status
            
        Returns:
            List of Task instances
        """
        try:
            query = {"user_id": user_id}
            if status:
                query["status"] = status
            
            tasks_data = self.collection.find(query).sort("created_at", -1)
            return [Task.from_dict(task_data) for task_data in tasks_data]
        except Exception as e:
            print(f"Error retrieving tasks by user: {e}")
            return []
    
    def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Task]:
        """
        Retrieve all tasks, optionally with filters.
        
        Args:
            filters: Optional dictionary of filters
            
        Returns:
            List of Task instances
        """
        try:
            query = filters or {}
            tasks_data = self.collection.find(query).sort("created_at", -1)
            return [Task.from_dict(task_data) for task_data in tasks_data]
        except Exception as e:
            print(f"Error retrieving all tasks: {e}")
            return []
    
    def get_by_priority(self, user_id: str, min_priority: int, max_priority: int) -> List[Task]:
        """
        Retrieve tasks by priority range.
        
        Args:
            user_id: User's unique identifier
            min_priority: Minimum priority level
            max_priority: Maximum priority level
            
        Returns:
            List of Task instances
        """
        try:
            query = {
                "user_id": user_id,
                "priority": {"$gte": min_priority, "$lte": max_priority}
            }
            tasks_data = self.collection.find(query).sort("priority", -1)
            return [Task.from_dict(task_data) for task_data in tasks_data]
        except Exception as e:
            print(f"Error retrieving tasks by priority: {e}")
            return []
    
    def get_by_label(self, user_id: str, label_name: str) -> List[Task]:
        """
        Retrieve tasks by label name.
        
        Args:
            user_id: User's unique identifier
            label_name: Name of the label to filter by
            
        Returns:
            List of Task instances
        """
        try:
            query = {
                "user_id": user_id,
                "labels.name": label_name
            }
            tasks_data = self.collection.find(query).sort("created_at", -1)
            return [Task.from_dict(task_data) for task_data in tasks_data]
        except Exception as e:
            print(f"Error retrieving tasks by label: {e}")
            return []
    
    def get_overdue_tasks(self, user_id: str) -> List[Task]:
        """
        Retrieve overdue tasks for a user.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            List of overdue Task instances
        """
        try:
            query = {
                "user_id": user_id,
                "due_date": {"$lt": datetime.now()},
                "status": {"$nin": ["completed", "deleted"]}
            }
            tasks_data = self.collection.find(query).sort("due_date", 1)
            return [Task.from_dict(task_data) for task_data in tasks_data]
        except Exception as e:
            print(f"Error retrieving overdue tasks: {e}")
            return []
    
    def update(self, task_id: str, update_data: Dict[str, Any]) -> bool:
        """
        Update a task's information.
        
        Args:
            task_id: Task's MongoDB ObjectId as string
            update_data: Dictionary of fields to update
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            # Remove fields that shouldn't be updated directly
            update_data.pop('_id', None)
            update_data.pop('user_id', None)  # user_id shouldn't change
            update_data.pop('created_at', None)  # created_at shouldn't change
            
            # Update the updated_at timestamp
            update_data['updated_at'] = datetime.now()
            
            result = self.collection.update_one(
                {"_id": ObjectId(task_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating task: {e}")
            return False
    
    def update_status(self, task_id: str, status: str) -> bool:
        """
        Update a task's status.
        
        Args:
            task_id: Task's MongoDB ObjectId as string
            status: New status
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        if status not in Task.VALID_STATUSES:
            raise ValueError(f"Invalid status. Must be one of: {Task.VALID_STATUSES}")
        
        return self.update(task_id, {"status": status})
    
    def add_dependency(self, task_id: str, dependency_id: str) -> bool:
        """
        Add a dependency to a task.
        
        Args:
            task_id: Task's MongoDB ObjectId as string
            dependency_id: ID of the task to depend on
            
        Returns:
            bool: True if addition was successful, False otherwise
        """
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(task_id)},
                {
                    "$addToSet": {"dependencies": dependency_id},
                    "$set": {"updated_at": datetime.now()}
                }
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error adding dependency: {e}")
            return False
    
    def remove_dependency(self, task_id: str, dependency_id: str) -> bool:
        """
        Remove a dependency from a task.
        
        Args:
            task_id: Task's MongoDB ObjectId as string
            dependency_id: ID of the dependency to remove
            
        Returns:
            bool: True if removal was successful, False otherwise
        """
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(task_id)},
                {
                    "$pull": {"dependencies": dependency_id},
                    "$set": {"updated_at": datetime.now()}
                }
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error removing dependency: {e}")
            return False
    
    def delete(self, task_id: str) -> bool:
        """
        Delete a task from the database.
        
        Args:
            task_id: Task's MongoDB ObjectId as string
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            result = self.collection.delete_one({"_id": ObjectId(task_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting task: {e}")
            return False
    
    def soft_delete(self, task_id: str) -> bool:
        """
        Soft delete a task by setting its status to 'deleted'.
        
        Args:
            task_id: Task's MongoDB ObjectId as string
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        return self.update_status(task_id, "deleted")
    
    def count_by_user(self, user_id: str, status: Optional[str] = None) -> int:
        """
        Count tasks for a specific user.
        
        Args:
            user_id: User's unique identifier
            status: Optional filter by status
            
        Returns:
            int: Count of tasks
        """
        try:
            query = {"user_id": user_id}
            if status:
                query["status"] = status
            return self.collection.count_documents(query)
        except Exception as e:
            print(f"Error counting tasks: {e}")
            return 0
    
    def get_task_statistics(self, user_id: str) -> Dict[str, int]:
        """
        Get task statistics for a user.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            Dictionary with task counts by status
        """
        try:
            stats = {
                "total": 0,
                "open": 0,
                "inprocess": 0,
                "completed": 0,
                "deleted": 0,
                "overdue": 0
            }
            
            stats["total"] = self.count_by_user(user_id)
            stats["open"] = self.count_by_user(user_id, "open")
            stats["inprocess"] = self.count_by_user(user_id, "inprocess")
            stats["completed"] = self.count_by_user(user_id, "completed")
            stats["deleted"] = self.count_by_user(user_id, "deleted")
            stats["overdue"] = len(self.get_overdue_tasks(user_id))
            
            return stats
        except Exception as e:
            print(f"Error getting task statistics: {e}")
            return {}
