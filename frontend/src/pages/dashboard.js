import React, { useEffect, useCallback, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { useAuth } from '../context/AuthContext';
import { useTask } from '../context/TaskContext';
// Removed withAuth import - handling auth manually
import MainLayout from '../layouts/MainLayout';
import Card from '../components/Card';
import TaskCard from '../components/TaskCard';
import Loader from '../components/Loader';
import ErrorMessage from '../components/ErrorMessage';
import { TASK_STATUS_OPTIONS } from '../constants';

const DashboardPage = () => {
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();
  const router = useRouter();
  
  // Debug authentication state (reduced logging to prevent spam)
  if (process.env.NODE_ENV === 'development') {
    console.log('Dashboard: Auth state:', {
      isAuthenticated,
      authLoading,
      user: user ? { username: user.username, id: user.id } : null
    });
  }
  const { 
    statistics, 
    tasks,
    fetchStatistics, 
    fetchTasks,
    isLoading, 
    error, 
    clearError 
  } = useTask();

  const [hasFetchedData, setHasFetchedData] = useState(false);

  // Removed manual authentication check to prevent infinite loop

  // If not authenticated, redirect to login immediately
  useEffect(() => {
    // Only redirect if we're sure the user is not authenticated and not loading
    if (!isAuthenticated && !authLoading) {
      console.log('Dashboard: User not authenticated, redirecting to login');
      router.push('/'); // Redirect to home page where login form is located
    }
  }, [isAuthenticated, authLoading, router]);

  // Fetch dashboard data when user is authenticated - SIMPLIFIED APPROACH
  useEffect(() => {
    if (isAuthenticated && !authLoading && user && !hasFetchedData) {
      console.log('Dashboard: Starting data fetch for user:', user.username);
      setHasFetchedData(true);
      
      const fetchDataSequentially = async () => {
        try {
          console.log('Dashboard: Step 1 - Fetching statistics...');
          await fetchStatistics();
          console.log('Dashboard: Step 1 - Statistics fetched successfully');
          
          console.log('Dashboard: Step 2 - Fetching tasks...');
          await fetchTasks({}, true);
          console.log('Dashboard: Step 2 - Tasks fetched successfully');
          
          console.log('Dashboard: All data fetched successfully');
        } catch (error) {
          console.error('Dashboard: Error fetching data:', error);
          setHasFetchedData(false);
        }
      };
      
      fetchDataSequentially();
    }
  }, [isAuthenticated, authLoading, user, hasFetchedData]);

  // Reset fetched data state when user changes
  useEffect(() => {
    if (user && user.username) {
      console.log('User changed, resetting fetch state for:', user.username);
      setHasFetchedData(false);
    }
  }, [user?.username]);

  // Reset fetched data state when user logs out
  useEffect(() => {
    if (!isAuthenticated) {
      setHasFetchedData(false);
    }
  }, [isAuthenticated]);

  const StatCard = ({ title, value, color = 'gray', icon }) => (
    <Card className="p-6">
      <div className="flex items-center">
        <div className="flex-shrink-0">
          <div className={`w-8 h-8 ${color} rounded-md flex items-center justify-center`}>
            {icon}
          </div>
        </div>
        <div className="ml-4">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-semibold text-gray-900">{value}</p>
        </div>
      </div>
    </Card>
  );

  const StatusCard = ({ status, count, color }) => (
    <Card className="p-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <div className={`w-3 h-3 ${color} rounded-full mr-3`}></div>
          <span className="text-sm font-medium text-gray-700">{status}</span>
        </div>
        <span className="text-lg font-semibold text-gray-900">{count}</span>
      </div>
    </Card>
  );

  // Show loading only during initial auth check or when fetching data for the first time
  if (authLoading || (!hasFetchedData && isAuthenticated && user)) {
    return (
      <MainLayout>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <Loader size="lg" text="Loading dashboard..." />
        </div>
      </MainLayout>
    );
  }

  // If not authenticated, show loading while redirecting
  if (!isAuthenticated && !authLoading) {
    return (
      <MainLayout>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">Authentication Required</h1>
            <p className="text-gray-600 mb-6">You need to log in to access the dashboard.</p>
            <Loader size="lg" text="Redirecting to login..." />
            <div className="mt-4">
              <Link href="/" className="text-blue-600 hover:text-blue-800">
                Or click here to go to login page
              </Link>
            </div>
          </div>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.first_name || user?.username || 'User'}!
          </h1>
          <p className="mt-2 text-gray-600">
            Here&apos;s an overview of your task management system.
          </p>
        </div>

        {error && (
          <div className="mb-6">
            <ErrorMessage
              message={error}
              onDismiss={clearError}
            />
          </div>
        )}

        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Total Tasks"
            value={statistics?.total || 0}
            color="bg-blue-100 text-white"
            icon={
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
              </svg>
            }
          />
          <StatCard
            title="Overdue Tasks"
            value={statistics?.overdue || 0}
            color="bg-red-100 text-red-600"
            icon={
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
              </svg>
            }
          />
          <StatCard
            title="High Priority"
            value={statistics?.high_priority_tasks || 0}
            color="bg-orange-100 text-orange-600"
            icon={
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd" />
              </svg>
            }
          />
          <StatCard
            title="Completed"
            value={statistics?.Complete || 0}
            color="bg-green-100 text-green-600"
            icon={
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
            }
          />
        </div>

        {/* Tasks by Status */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <Card>
            <Card.Header>
              <Card.Title>Tasks by Status</Card.Title>
              <Card.Description>
                Distribution of tasks across different statuses
              </Card.Description>
            </Card.Header>
            <Card.Content>
              <div className="space-y-3">
                {TASK_STATUS_OPTIONS.map((status) => {
                  const count = statistics?.[status.value] || 0;
                  return (
                    <StatusCard
                      key={status.value}
                      status={status.label}
                      count={count}
                      color={status.color}
                    />
                  );
                })}
              </div>
            </Card.Content>
          </Card>

          {/* Quick Actions */}
          <Card>
            <Card.Header>
              <Card.Title>Quick Actions</Card.Title>
              <Card.Description>
                Common tasks and shortcuts
              </Card.Description>
            </Card.Header>
            <Card.Content>
              <div className="space-y-4">
                <Link
                  href="/tasks/new"
                  className="block p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center">
                    <div className="w-8 h-8 bg-blue-100 rounded-md flex items-center justify-center mr-3">
                      <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div>
                      <h3 className="text-sm font-medium text-gray-900">Create New Task</h3>
                      <p className="text-sm text-gray-500">Add a new task to your list</p>
                    </div>
                  </div>
                </Link>

                <Link
                  href="/tasks"
                  className="block p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center">
                    <div className="w-8 h-8 bg-green-100 rounded-md flex items-center justify-center mr-3">
                      <svg className="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div>
                      <h3 className="text-sm font-medium text-gray-900">View All Tasks</h3>
                      <p className="text-sm text-gray-500">Manage and organize your tasks</p>
                    </div>
                  </div>
                </Link>

              </div>
            </Card.Content>
          </Card>
        </div>

        {/* Recent Tasks */}
        <div className="mt-8">
          <Card>
            <Card.Header>
              <Card.Title>Recent Tasks</Card.Title>
              <Card.Description>
                Your most recent tasks
              </Card.Description>
            </Card.Header>
            <Card.Content>
              {isLoading ? (
                <div className="flex justify-center py-8">
                  <Loader size="md" text="Loading tasks..." />
                </div>
              ) : tasks && tasks.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {tasks.slice(0, 6).map((task) => (
                    <TaskCard
                      key={task.id}
                      task={task}
                      onEdit={(task) => {
                        router.push(`/tasks/${task.id}/edit`);
                      }}
                      onDelete={() => {
                        // Handle delete if needed
                        console.log('Delete task:', task.id);
                      }}
                    />
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
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
                    <Link
                      href="/tasks/new"
                      className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-gray-900 hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                    >
                      Create Task
                    </Link>
                  </div>
                </div>
              )}
              
              {tasks && tasks.length > 6 && (
                <div className="mt-6 text-center">
                  <Link
                    href="/tasks"
                    className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                  >
                    View All Tasks ({tasks.length})
                  </Link>
                </div>
              )}
            </Card.Content>
          </Card>
        </div>
      </div>
    </MainLayout>
  );
};

export default DashboardPage;
