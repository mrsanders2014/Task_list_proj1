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
    if (!dateString) return 'No due date';
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
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-lg font-semibold text-gray-900 line-clamp-2">
          {task.title}
        </h3>
        <div className="flex space-x-2 ml-4">
          <StatusBadge status={task.status} />
          {task.task_mgmt?.priority && (
            <PriorityBadge priority={task.task_mgmt.priority} />
          )}
        </div>
      </div>
      
      {task.description && (
        <p className="text-gray-600 text-sm mb-3 line-clamp-3">
          {task.description}
        </p>
      )}
      
      <div className="flex flex-wrap gap-2 mb-3">
        {task.labels?.map((label, index) => (
          <span
            key={index}
            className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
            style={{ backgroundColor: label.color + '20', color: label.color }}
          >
            {label.name}
          </span>
        ))}
      </div>
      
      <div className="flex justify-between items-center text-sm text-gray-500 mb-3">
        <div>
          <span className="font-medium">Created:</span> {formatDate(task.createdate)}
        </div>
        {task.task_mgmt?.duedate && (
          <div className={`font-medium ${isOverdue() ? 'text-red-600' : 'text-gray-500'}`}>
            <span>Due:</span> {formatDate(task.task_mgmt.duedate)}
            {isOverdue() && <span className="ml-1">(Overdue)</span>}
          </div>
        )}
      </div>
      
      {task.task_mgmt?.estimated_time_to_complete && (
        <div className="text-sm text-gray-500 mb-3">
          <span className="font-medium">Est. Time:</span> {task.task_mgmt.estimated_time_to_complete} hours
        </div>
      )}
      
      {showActions && (
        <div className="flex justify-end space-x-2 pt-3 border-t border-gray-200">
          <Button
            variant="outline"
            size="sm"
            onClick={() => onEdit?.(task)}
          >
            Edit
          </Button>
          <Button
            variant="danger"
            size="sm"
            onClick={() => onDelete?.(task)}
          >
            Delete
          </Button>
        </div>
      )}
    </Card>
  );
};

export default TaskCard;
