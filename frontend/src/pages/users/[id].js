import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '../../context/AuthContext';
import { useTask } from '../../context/TaskContext';
import { withAuth } from '../../middleware/authMiddleware';
import MainLayout from '../../layouts/MainLayout';
import Card from '../../components/Card';
import TaskCard from '../../components/TaskCard';
import Button from '../../components/Button';
import Loader from '../../components/Loader';
import ErrorMessage from '../../components/ErrorMessage';
import userService from '../../services/userService';
import { format } from 'date-fns';

const UserProfilePage = () => {
  const { user: currentUser } = useAuth();
  const { fetchTasks, tasks } = useTask();
  const router = useRouter();
  const { id } = router.query;
  const [user, setUser] = useState(null);
  const [userTasks, setUserTasks] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (id) {
      fetchUser();
      fetchUserTasks();
    }
  }, [id]);

  const fetchUser = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const userData = await userService.getUser(id);
      setUser(userData);
    } catch (error) {
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchUserTasks = async () => {
    try {
      const tasks = await userService.getUserTasks(id);
      setUserTasks(tasks);
    } catch (error) {
      console.error('Error fetching user tasks:', error);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Never';
    try {
      return format(new Date(dateString), 'PPP');
    } catch {
      return 'Invalid date';
    }
  };

  if (isLoading) {
    return (
      <MainLayout>
        <div className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
          <Loader size="lg" text="Loading user profile..." />
        </div>
      </MainLayout>
    );
  }

  if (!user) {
    return (
      <MainLayout>
        <div className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="text-center py-12">
            <h3 className="text-lg font-medium text-gray-900">User not found</h3>
            <p className="mt-1 text-sm text-gray-500">
              The user you&apos;re looking for doesn&apos;t exist or has been deleted.
            </p>
            <div className="mt-6">
              <Button onClick={() => router.push('/users')}>
                Back to Users
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
            <div className="flex items-center">
              <div className="w-16 h-16 bg-gray-900 rounded-full flex items-center justify-center mr-4">
                <span className="text-xl font-medium text-white">
                  {user.first_name?.[0] || user.username[0]}
                </span>
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  {user.first_name && user.last_name 
                    ? `${user.first_name} ${user.last_name}`
                    : user.username
                  }
                </h1>
                <div className="mt-2 flex items-center space-x-4">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-sm font-medium ${
                    user.is_active 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {user.is_active ? 'Active' : 'Inactive'}
                  </span>
                  <span className="text-sm text-gray-500">@{user.username}</span>
                </div>
              </div>
            </div>
            <Button
              variant="outline"
              onClick={() => router.push('/users')}
            >
              Back to Users
            </Button>
          </div>
        </div>

        {error && (
          <div className="mb-6">
            <ErrorMessage
              message={error}
              onDismiss={() => setError(null)}
            />
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* User Information */}
          <div className="lg:col-span-1">
            <Card>
              <Card.Header>
                <Card.Title>User Information</Card.Title>
              </Card.Header>
              <Card.Content>
                <dl className="space-y-4">
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Username</dt>
                    <dd className="mt-1 text-sm text-gray-900">{user.username}</dd>
                  </div>
                  
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Email</dt>
                    <dd className="mt-1 text-sm text-gray-900">{user.email}</dd>
                  </div>
                  
                  {user.first_name && (
                    <div>
                      <dt className="text-sm font-medium text-gray-500">First Name</dt>
                      <dd className="mt-1 text-sm text-gray-900">{user.first_name}</dd>
                    </div>
                  )}
                  
                  {user.last_name && (
                    <div>
                      <dt className="text-sm font-medium text-gray-500">Last Name</dt>
                      <dd className="mt-1 text-sm text-gray-900">{user.last_name}</dd>
                    </div>
                  )}
                  
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Status</dt>
                    <dd className="mt-1">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        user.is_active 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {user.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </dd>
                  </div>
                  
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Member Since</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {formatDate(user.created_at)}
                    </dd>
                  </div>
                  
                  {user.last_login && (
                    <div>
                      <dt className="text-sm font-medium text-gray-500">Last Login</dt>
                      <dd className="mt-1 text-sm text-gray-900">
                        {formatDate(user.last_login)}
                      </dd>
                    </div>
                  )}
                </dl>
              </Card.Content>
            </Card>
          </div>

          {/* User Tasks */}
          <div className="lg:col-span-2">
            <Card>
              <Card.Header>
                <Card.Title>User Tasks</Card.Title>
                <Card.Description>
                  {userTasks.length} task{userTasks.length !== 1 ? 's' : ''} assigned to this user
                </Card.Description>
              </Card.Header>
              <Card.Content>
                {userTasks.length === 0 ? (
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
                      This user hasn&apos;t been assigned any tasks yet.
                    </p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 gap-4">
                    {userTasks.slice(0, 5).map((task) => (
                      <TaskCard
                        key={task.id}
                        task={task}
                        showActions={false}
                        className="border border-gray-200"
                      />
                    ))}
                    {userTasks.length > 5 && (
                      <div className="text-center pt-4">
                        <Button
                          variant="outline"
                          onClick={() => router.push(`/tasks?user_id=${user.id}`)}
                        >
                          View All Tasks ({userTasks.length})
                        </Button>
                      </div>
                    )}
                  </div>
                )}
              </Card.Content>
            </Card>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default withAuth(UserProfilePage);
