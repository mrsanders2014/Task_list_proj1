import React, { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/router';
import { useTask } from '../../context/TaskContext';
import { useAuth } from '../../context/AuthContext';
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
  
  const { logout, isAuthenticated, user, isLoading: authLoading } = useAuth();
  const router = useRouter();

  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const hasFetchedTasks = useRef(false);

  useEffect(() => {
    // Early return if not authenticated or still loading - don't make any API calls
    if (!isAuthenticated || authLoading || !user || !user.id) {
      return;
    }
    
    // Only fetch tasks if we haven't fetched yet
    if (!hasFetchedTasks.current) {
      hasFetchedTasks.current = true;
      fetchTasks({}, false); // Don't force refresh to prevent infinite loops
    }
  }, [isAuthenticated, user?.id, authLoading]); // Use user.id instead of user object to prevent unnecessary re-renders

  // Reset the fetch flag when user changes (for logout/login scenarios)
  useEffect(() => {
    if (!isAuthenticated || !user) {
      hasFetchedTasks.current = false;
    }
  }, [isAuthenticated, user]);

  const handleCreateTask = async (taskData) => {
    try {
      setIsSubmitting(true);
      await createTask(taskData);
      setIsCreateModalOpen(false);
      // Try to refresh tasks, but don't fail if it doesn't work
      try {
        await fetchTasks({}, true); // Force refresh the list
      } catch (refreshError) {
        // Still show success to user since task was created
      }
    } catch (error) {
      // Don't close modal on error so user can try again
    } finally {
      setIsSubmitting(false);
    }
  };


  const handleDeleteTask = async (task) => {
    if (window.confirm(`Are you sure you want to delete "${task.title}"?`)) {
      try {
        await deleteTask(task.id);
        fetchTasks({}, true); // Force refresh the list
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
    fetchTasks({}, true);
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

  const handleLogout = async () => {
    try {
      await logout();
      router.push('/');
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  // Don't render if not authenticated or still loading
  if (authLoading) {
    return (
      <MainLayout showFooter={false}>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900"></div>
          </div>
        </div>
      </MainLayout>
    );
  }

  if (!isAuthenticated || !user) {
    return (
      <MainLayout showFooter={false}>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900">Please log in to view tasks</h1>
            <p className="mt-2 text-gray-600">You need to be authenticated to access this page.</p>
          </div>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout showFooter={false}>
      <div 
        className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8 tasks-page"
        style={{ 
          backgroundColor: 'transparent',
          backgroundImage: 'none'
        }}
      >
        {/* Header */}
        <div className="mb-8">
          <div className="flex justify-between items-center">
            <div>
              <p className="mt-2 text-white" style={{ fontSize: '20pt', color: 'white !important' }}>
                Manage and organize your tasks
              </p>
            </div>
            <Button 
              onClick={() => {
                if (isCreateModalOpen) {
                  return;
                }
                setIsCreateModalOpen(true);
              }}
              className="text-white"
              style={{ 
                fontSize: '20pt',
                color: 'white !important',
                backgroundColor: 'transparent',
                border: '2px solid white'
              }}
            >
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
              <Button 
                variant="outline" 
                onClick={clearFilters}
                style={{ 
                  fontSize: '20pt',
                  color: 'white !important',
                  borderColor: 'white',
                  backgroundColor: 'transparent'
                }}
              >
                Clear Filters
              </Button>
              <Button 
                onClick={handleSearch}
                style={{ 
                  fontSize: '20pt',
                  color: 'white !important',
                  backgroundColor: 'transparent',
                  border: '2px solid white'
                }}
              >
                Apply Filters
              </Button>
            </div>
          </div>
        </Card>

        {/* Tasks List */}
        {isLoading ? (
          <div className="flex justify-center items-center py-8">
            <div className="text-white text-lg">Loading tasks...</div>
          </div>
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
                  <Button 
                    onClick={() => setIsCreateModalOpen(true)}
                    style={{ 
                      fontSize: '20pt',
                      color: 'white !important',
                      backgroundColor: 'transparent',
                      border: '2px solid white'
                    }}
                  >
                    Create Task
                  </Button>
                </div>
              </div>
            ) : (
              tasks.map((task) => (
                <TaskCard
                  key={task.id}
                  task={task}
                  onEdit={(task) => router.push(`/tasks/${task.id}/edit`)}
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


        {/* Logout Button */}
        <div className="mt-8 pt-6 border-t border-gray-200">
          <div className="flex justify-center">
            <Button
              variant="outline"
              onClick={handleLogout}
              className="logout-button"
              style={{ 
                fontSize: '20pt',
                color: 'red !important',
                borderColor: 'red',
                backgroundColor: 'transparent'
              }}
            >
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Logout
            </Button>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default withAuth(TasksPage);
