import React, { useState, useEffect } from 'react';
import { useTask } from '../../context/TaskContext';
import { withAuth } from '../../middleware/authMiddleware';
import MainLayout from '../../layouts/MainLayout';
import Card from '../../components/Card';
import TaskCard from '../../components/TaskCard';
import Modal from '../../components/Modal';
import TaskForm from '../../components/TaskForm';
import Button from '../../components/Button';
import Input from '../../components/Input';
import Loader from '../../components/Loader';
import ErrorMessage from '../../components/ErrorMessage';
import { TASK_STATUS_OPTIONS, PRIORITY_OPTIONS } from '../../constants';

const TasksPage = () => {
  const {
    tasks,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    isLoading,
    error,
    clearError,
    filters,
    setFilters,
    pagination,
    setPagination,
  } = useTask();

  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const handleCreateTask = async (taskData) => {
    try {
      setIsSubmitting(true);
      await createTask(taskData);
      setIsCreateModalOpen(false);
      fetchTasks(); // Refresh the list
    } catch (error) {
      console.error('Error creating task:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleEditTask = async (taskData) => {
    try {
      setIsSubmitting(true);
      await updateTask(editingTask.id, taskData);
      setEditingTask(null);
      fetchTasks(); // Refresh the list
    } catch (error) {
      console.error('Error updating task:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDeleteTask = async (task) => {
    if (window.confirm(`Are you sure you want to delete "${task.title}"?`)) {
      try {
        await deleteTask(task.id);
        fetchTasks(); // Refresh the list
      } catch (error) {
        console.error('Error deleting task:', error);
      }
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters({ [key]: value });
    setPagination({ currentPage: 1 }); // Reset to first page
  };

  const handleSearch = () => {
    fetchTasks();
  };

  const clearFilters = () => {
    setFilters({
      task_status: '',
      min_priority: '',
      max_priority: '',
      label_name: '',
      overdue_only: false,
    });
    setPagination({ currentPage: 1 });
  };

  return (
    <MainLayout>
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Tasks</h1>
              <p className="mt-2 text-gray-600">
                Manage and organize your tasks
              </p>
            </div>
            <Button onClick={() => setIsCreateModalOpen(true)}>
              Create Task
            </Button>
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

        {/* Filters */}
        <Card className="mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Status
              </label>
              <select
                value={filters.task_status}
                onChange={(e) => handleFilterChange('task_status', e.target.value)}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500"
              >
                <option value="">All Statuses</option>
                {TASK_STATUS_OPTIONS.map((status) => (
                  <option key={status.value} value={status.value}>
                    {status.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Min Priority
              </label>
              <select
                value={filters.min_priority}
                onChange={(e) => handleFilterChange('min_priority', e.target.value)}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500"
              >
                <option value="">Any Priority</option>
                {PRIORITY_OPTIONS.map((priority) => (
                  <option key={priority.value} value={priority.value}>
                    {priority.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Max Priority
              </label>
              <select
                value={filters.max_priority}
                onChange={(e) => handleFilterChange('max_priority', e.target.value)}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500"
              >
                <option value="">Any Priority</option>
                {PRIORITY_OPTIONS.map((priority) => (
                  <option key={priority.value} value={priority.value}>
                    {priority.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Label
              </label>
              <Input
                value={filters.label_name}
                onChange={(e) => handleFilterChange('label_name', e.target.value)}
                placeholder="Filter by label"
              />
            </div>
          </div>

          <div className="flex justify-between items-center mt-4">
            <div className="flex items-center">
              <input
                type="checkbox"
                id="overdue_only"
                checked={filters.overdue_only}
                onChange={(e) => handleFilterChange('overdue_only', e.target.checked)}
                className="h-4 w-4 text-gray-600 focus:ring-gray-500 border-gray-300 rounded"
              />
              <label htmlFor="overdue_only" className="ml-2 block text-sm text-gray-700">
                Show only overdue tasks
              </label>
            </div>
            
            <div className="flex space-x-2">
              <Button variant="outline" onClick={clearFilters}>
                Clear Filters
              </Button>
              <Button onClick={handleSearch}>
                Apply Filters
              </Button>
            </div>
          </div>
        </Card>

        {/* Tasks List */}
        {isLoading ? (
          <Loader size="lg" text="Loading tasks..." />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {tasks.length === 0 ? (
              <div className="col-span-full text-center py-12">
                <svg
                  className="mx-auto h-12 w-12 text-gray-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                  />
                </svg>
                <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks found</h3>
                <p className="mt-1 text-sm text-gray-500">
                  Get started by creating a new task.
                </p>
                <div className="mt-6">
                  <Button onClick={() => setIsCreateModalOpen(true)}>
                    Create Task
                  </Button>
                </div>
              </div>
            ) : (
              tasks.map((task) => (
                <TaskCard
                  key={task.id}
                  task={task}
                  onEdit={setEditingTask}
                  onDelete={handleDeleteTask}
                />
              ))
            )}
          </div>
        )}

        {/* Create Task Modal */}
        <Modal
          isOpen={isCreateModalOpen}
          onClose={() => setIsCreateModalOpen(false)}
          title="Create New Task"
          size="lg"
        >
          <TaskForm
            onSubmit={handleCreateTask}
            onCancel={() => setIsCreateModalOpen(false)}
            isLoading={isSubmitting}
          />
        </Modal>

        {/* Edit Task Modal */}
        <Modal
          isOpen={!!editingTask}
          onClose={() => setEditingTask(null)}
          title="Edit Task"
          size="lg"
        >
          <TaskForm
            task={editingTask}
            onSubmit={handleEditTask}
            onCancel={() => setEditingTask(null)}
            isLoading={isSubmitting}
          />
        </Modal>
      </div>
    </MainLayout>
  );
};

export default withAuth(TasksPage);
