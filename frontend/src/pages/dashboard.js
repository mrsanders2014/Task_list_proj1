import React, { useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '../context/AuthContext';
import { useTask } from '../context/TaskContext';
import { withAuth } from '../middleware/authMiddleware';
import MainLayout from '../layouts/MainLayout';
import Card from '../components/Card';
import Loader from '../components/Loader';
import ErrorMessage from '../components/ErrorMessage';
import { TASK_STATUS_OPTIONS } from '../constants';

const DashboardPage = () => {
  const { user } = useAuth();
  const { 
    statistics, 
    fetchStatistics, 
    isLoading, 
    error, 
    clearError 
  } = useTask();

  useEffect(() => {
    fetchStatistics();
  }, [fetchStatistics]);

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

  if (isLoading) {
    return (
      <MainLayout>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <Loader size="lg" text="Loading dashboard..." />
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
            value={statistics?.total_tasks || 0}
            color="bg-blue-100 text-white"
            icon={
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
              </svg>
            }
          />
          <StatCard
            title="Overdue Tasks"
            value={statistics?.overdue_tasks || 0}
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
            value={statistics?.tasks_by_status?.Complete || 0}
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
                  const count = statistics?.tasks_by_status?.[status.value] || 0;
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

                <Link
                  href="/users"
                  className="block p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center">
                    <div className="w-8 h-8 bg-purple-100 rounded-md flex items-center justify-center mr-3">
                      <svg className="w-5 h-5 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
                      </svg>
                    </div>
                    <div>
                      <h3 className="text-sm font-medium text-gray-900">Manage Users</h3>
                      <p className="text-sm text-gray-500">View and manage user accounts</p>
                    </div>
                  </div>
                </Link>
              </div>
            </Card.Content>
          </Card>
        </div>
      </div>
    </MainLayout>
  );
};

export default withAuth(DashboardPage);
