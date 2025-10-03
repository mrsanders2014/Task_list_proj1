"""
Task repository for CRUD operations on tasks
"""

import os
from typing import List, Optional, Dict, Any
from bson import ObjectId
from pymongo.collection import Collection
from dotenv import load_dotenv

from ..model.Task_class import Task
from .mongodb_client import get_mongo_client


class TaskRepository:
    """Repository for Task CRUD operations"""
    
    def __init__(self):
        """Initialize the task repository"""
        load_dotenv()
        self.client = get_mongo_client()
        collection_name = os.getenv('COLLECTION_NAME', 'tasks')
        self.collection: Collection = self.client.get_collection(collection_name)
    
    def create(self, task: Task) -> str:
        """
        Create a new task in the database
        
        Args:
            task: Task object to create
            
        Returns:
            str: ID of the created task
        """
        try:
            task_dict = task.to_dict()
            # Remove _id if it's None
            if task_dict.get('_id') is None:
                task_dict.pop('_id', None)
            
            result = self.collection.insert_one(task_dict)
            return str(result.inserted_id)
        except Exception as e:
            raise RuntimeError(f"Error creating task: {e}")
    
    def read(self, task_id: str) -> Optional[Task]:
        """
        Read a task by ID
        
        Args:
            task_id: ID of the task to read
            
        Returns:
            Task object or None if not found
        """
        try:
            result = self.collection.find_one({"_id": ObjectId(task_id)})
            if result:
                return Task.from_dict(result)
            return None
        except Exception as e:
            raise RuntimeError(f"Error reading task: {e}")
    
    def read_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Task]:
        """
        Read all tasks with optional filters
        
        Args:
            filters: Optional dictionary of filters
            
        Returns:
            List of Task objects
        """
        try:
            query = filters or {}
            results = self.collection.find(query)
            return [Task.from_dict(doc) for doc in results]
        except Exception as e:
            raise RuntimeError(f"Error reading tasks: {e}")
    
    def update(self, task_id: str, update_data: Dict[str, Any]) -> bool:
        """
        Update a task by ID
        
        Args:
            task_id: ID of the task to update
            update_data: Dictionary of fields to update
            
        Returns:
            bool: True if updated, False if not found
        """
        try:
            # Remove fields that shouldn't be updated
            update_data.pop('_id', None)
            update_data.pop('created_at', None)
            
            result = self.collection.update_one(
                {"_id": ObjectId(task_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            raise RuntimeError(f"Error updating task: {e}")
    
    def delete(self, task_id: str) -> bool:
        """
        Delete a task by ID
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        try:
            result = self.collection.delete_one({"_id": ObjectId(task_id)})
            return result.deleted_count > 0
        except Exception as e:
            raise RuntimeError(f"Error deleting task: {e}")
    
    def delete_all(self) -> int:
        """
        Delete all tasks (use with caution!)
        
        Returns:
            int: Number of tasks deleted
        """
        try:
            result = self.collection.delete_many({})
            return result.deleted_count
        except Exception as e:
            raise RuntimeError(f"Error deleting all tasks: {e}")
    
    def search(self, query: str, field: str = "title") -> List[Task]:
        """
        Search tasks by field using regex
        
        Args:
            query: Search query string
            field: Field to search in (default: title)
            
        Returns:
            List of matching Task objects
        """
        try:
            regex_query = {"$regex": query, "$options": "i"}
            results = self.collection.find({field: regex_query})
            return [Task.from_dict(doc) for doc in results]
        except Exception as e:
            raise RuntimeError(f"Error searching tasks: {e}")
    
    def get_by_status(self, status: str) -> List[Task]:
        """
        Get all tasks with a specific status
        
        Args:
            status: Task status to filter by
            
        Returns:
            List of Task objects
        """
        return self.read_all({"status": status})
    
    def get_by_priority(self, priority: str) -> List[Task]:
        """
        Get all tasks with a specific priority
        
        Args:
            priority: Task priority to filter by
            
        Returns:
            List of Task objects
        """
        return self.read_all({"priority": priority})

