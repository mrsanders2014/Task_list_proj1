import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { useTask } from '../../context/TaskContext';
import { withAuth } from '../../middleware/authMiddleware';
import MainLayout from '../../layouts/MainLayout';
import Card from '../../components/Card';
import TaskForm from '../../components/TaskForm';
import Button from '../../components/Button';
import Loader from '../../components/Loader';
import ErrorMessage from '../../components/ErrorMessage';
import StatusBadge from '../../components/StatusBadge';
import PriorityBadge from '../../components/PriorityBadge';
import { format } from 'date-fns';

const TaskDetailPage = () => {
  const { currentTask, fetchTask, updateTask, deleteTask, isLoading, error, clearError } = useTask();
  const router = useRouter();
  const { id } = router.query;
  const [isEditing, setIsEditing] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (id) {
      fetchTask(id);
    }
  }, [id, fetchTask]);

  const handleUpdate = async (taskData) => {
    try {
      setIsSubmitting(true);
      await updateTask(id, taskData);
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating task:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete "${currentTask?.title}"?`)) {
      try {
        await deleteTask(id);
        router.push('/tasks');
      } catch (error) {
        console.error('Error deleting task:', error);
      }
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Not set';
    try {
      return format(new Date(dateString), 'PPP');
    } catch {
      return 'Invalid date';
    }
  };

  const isOverdue = () => {
    if (!currentTask?.task_mgmt?.duedate) return false;
    return new Date(currentTask.task_mgmt.duedate) < new Date();
  };

  if (isLoading) {
    return (
      <MainLayout>
        <div className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
          <Loader size="lg" text="Loading task..." />
        </div>
      </MainLayout>
    );
  }

  if (!currentTask) {
    return (
      <MainLayout>
        <div className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="text-center py-12">
            <h3 className="text-lg font-medium text-gray-900">Task not found</h3>
            <p className="mt-1 text-sm text-gray-500">
              The task you&apos;re looking for doesn&apos;t exist or has been deleted.
            </p>
            <div className="mt-6">
              <Button onClick={() => router.push('/tasks')}>
                Back to Tasks
              </Button>
            </div>
          </div>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{currentTask.title}</h1>
              <div className="mt-2 flex items-center space-x-4">
                <StatusBadge status={currentTask.status} size="md" />
                {currentTask.task_mgmt?.priority && (
                  <PriorityBadge priority={currentTask.task_mgmt.priority} size="md" />
                )}
              </div>
            </div>
            <div className="flex space-x-2">
              <Button
                variant="outline"
                onClick={() => setIsEditing(!isEditing)}
              >
                {isEditing ? 'Cancel Edit' : 'Edit Task'}
              </Button>
              <Button
                variant="danger"
                onClick={handleDelete}
              >
                Delete
              </Button>
            </div>
          </div>
        </div>

        {error && (
          <div className="mb-6">
            <ErrorMessage
              message={error}
              onDismiss={clearError}
            />
          </div>
        )}

        {isEditing ? (
          /* Edit Form */
          <Card>
            <TaskForm
              task={currentTask}
              onSubmit={handleUpdate}
              onCancel={() => setIsEditing(false)}
              isLoading={isSubmitting}
            />
          </Card>
        ) : (
          /* Task Details */
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Main Content */}
            <div className="lg:col-span-2 space-y-6">
              <Card>
                <Card.Header>
                  <Card.Title>Description</Card.Title>
                </Card.Header>
                <Card.Content>
                  <p className="text-gray-700 whitespace-pre-wrap">
                    {currentTask.description || 'No description provided'}
                  </p>
                </Card.Content>
              </Card>

              {/* Labels */}
              {currentTask.labels && currentTask.labels.length > 0 && (
                <Card>
                  <Card.Header>
                    <Card.Title>Labels</Card.Title>
                  </Card.Header>
                  <Card.Content>
                    <div className="flex flex-wrap gap-2">
                      {currentTask.labels.map((label, index) => (
                        <span
                          key={index}
                          className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
                          style={{ backgroundColor: label.color + '20', color: label.color }}
                        >
                          {label.name}
                        </span>
                      ))}
                    </div>
                  </Card.Content>
                </Card>
              )}
            </div>

            {/* Sidebar */}
            <div className="space-y-6">
              {/* Task Information */}
              <Card>
                <Card.Header>
                  <Card.Title>Task Information</Card.Title>
                </Card.Header>
                <Card.Content>
                  <dl className="space-y-4">
                    <div>
                      <dt className="text-sm font-medium text-gray-500">Status</dt>
                      <dd className="mt-1">
                        <StatusBadge status={currentTask.status} />
                      </dd>
                    </div>
                    
                    {currentTask.task_mgmt?.priority && (
                      <div>
                        <dt className="text-sm font-medium text-gray-500">Priority</dt>
                        <dd className="mt-1">
                          <PriorityBadge priority={currentTask.task_mgmt.priority} />
                        </dd>
                      </div>
                    )}
                    
                    <div>
                      <dt className="text-sm font-medium text-gray-500">Created</dt>
                      <dd className="mt-1 text-sm text-gray-900">
                        {formatDate(currentTask.createdate)}
                      </dd>
                    </div>
                    
                    <div>
                      <dt className="text-sm font-medium text-gray-500">Last Modified</dt>
                      <dd className="mt-1 text-sm text-gray-900">
                        {formatDate(currentTask.lastmoddate)}
                      </dd>
                    </div>
                  </dl>
                </Card.Content>
              </Card>

              {/* Due Date & Time */}
              {(currentTask.task_mgmt?.duedate || currentTask.task_mgmt?.estimated_time_to_complete) && (
                <Card>
                  <Card.Header>
                    <Card.Title>Timeline</Card.Title>
                  </Card.Header>
                  <Card.Content>
                    <dl className="space-y-4">
                      {currentTask.task_mgmt?.duedate && (
                        <div>
                          <dt className="text-sm font-medium text-gray-500">Due Date</dt>
                          <dd className={`mt-1 text-sm font-medium ${
                            isOverdue() ? 'text-red-600' : 'text-gray-900'
                          }`}>
                            {formatDate(currentTask.task_mgmt.duedate)}
                            {isOverdue() && <span className="ml-1">(Overdue)</span>}
                          </dd>
                        </div>
                      )}
                      
                      {currentTask.task_mgmt?.estimated_time_to_complete && (
                        <div>
                          <dt className="text-sm font-medium text-gray-500">Estimated Time</dt>
                          <dd className="mt-1 text-sm text-gray-900">
                            {currentTask.task_mgmt.estimated_time_to_complete} hours
                          </dd>
                        </div>
                      )}
                    </dl>
                  </Card.Content>
                </Card>
              )}
            </div>
          </div>
        )}
      </div>
    </MainLayout>
  );
};

export default withAuth(TaskDetailPage);
