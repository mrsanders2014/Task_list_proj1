import React from 'react';
import { format } from 'date-fns';
import Card from './Card';
import StatusBadge from './StatusBadge';
import PriorityBadge from './PriorityBadge';
import Button from './Button';

const TaskCard = ({
  task,
  onEdit,
  onDelete,
  onStatusChange,
  showActions = true,
  className = '',
}) => {
  const formatDate = (dateString) => {
    if (!dateString) return 'No date';
    try {
      return format(new Date(dateString), 'MMM dd, yyyy');
    } catch {
      return 'Invalid date';
    }
  };

  const isOverdue = () => {
    if (!task.task_mgmt?.duedate) return false;
    return new Date(task.task_mgmt.duedate) < new Date();
  };

  return (
    <Card className={`hover:shadow-lg transition-shadow ${className}`}>
      {/* First line: Task Title */}
      <div className="flex items-center mb-2">
        <span 
          className="text-gray-400 font-medium mr-2"
          style={{ fontSize: '18pt' }}
        >
          Task Title:
        </span>
        <h3 className="text-lg font-semibold text-gray-900 line-clamp-2">
          {task.title}
        </h3>
      </div>
      
      {/* Second line: Description */}
      <div className="mb-2">
        <span className="font-medium text-gray-500">Description: </span>
        <span className="text-gray-600 text-sm">
          {task.description || 'No description'}
        </span>
      </div>
      
      {/* Third line: Priority */}
      <div className="mb-3">
        <span className="font-medium text-gray-500">Priority: </span>
        {task.task_mgmt?.priority ? (
          <PriorityBadge priority={task.task_mgmt.priority} />
        ) : (
          <span className="text-gray-400 text-sm">No priority set</span>
        )}
      </div>
      
      {/* Fourth line: Status */}
      <div className="mb-3">
        <span className="font-medium text-gray-500">Status: </span>
        <StatusBadge status={task.status} />
      </div>
      
      <div className="mb-3">
        <div className="flex items-center flex-wrap gap-2">
          <span className="font-medium text-gray-500">Label(s): </span>
          {task.labels && task.labels.length > 0 ? (
            task.labels.map((label, index) => (
              <span key={index}>
                <span
                  className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
                  style={{ backgroundColor: label.color + '20', color: label.color }}
                >
                  {label.name}
                </span>
                {index < task.labels.length - 1 && <span className="text-gray-500">, </span>}
              </span>
            ))
          ) : (
            <span className="text-gray-400 text-sm">No labels</span>
          )}
        </div>
      </div>
      
      <div className="text-sm text-gray-500 mb-3">
        <div className="flex items-center justify-start w-full">
          <div className="flex-1">
            <span className="font-medium">Due Date: </span>
            <span>{formatDate(task.task_mgmt?.duedate)}</span>
            {isOverdue() && <span className="ml-1 text-red-600">(Overdue)</span>}
          </div>
          <div className="flex-1">
            <span className="font-medium">Last update date: </span>
            <span>{formatDate(task.lastmoddate)}</span>
          </div>
          <div className="flex-1">
            <span className="font-medium">Created on: </span>
            <span>{formatDate(task.createdate)}</span>
          </div>
        </div>
      </div>
      
      {task.task_mgmt?.estimated_time_to_complete && (
        <div className="text-sm text-gray-500 mb-3">
          <span className="font-medium">Est. Time: </span>{task.task_mgmt.estimated_time_to_complete} hours
        </div>
      )}
      
      {showActions && (
        <div className="flex justify-end space-x-2 pt-3 border-t border-gray-200">
          <Button
            variant="outline"
            size="sm"
            className="edit-button"
            onClick={() => {
              // Edit button clicked
              onEdit?.(task);
            }}
            style={{
              color: '#FFD700 !important',
              borderColor: '#FFD700',
              backgroundColor: 'transparent'
            }}
          >
            Edit
          </Button>
          <Button
            variant="danger"
            size="sm"
            className="delete-button"
            onClick={() => onDelete?.(task)}
            style={{
              color: '#FFD700 !important',
              borderColor: '#FFD700',
              backgroundColor: 'transparent'
            }}
          >
            Delete
          </Button>
        </div>
      )}
    </Card>
  );
};

export default TaskCard;
