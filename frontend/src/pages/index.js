import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { useForm } from 'react-hook-form';
import Card from '../components/Card';
import Input from '../components/Input';
import Button from '../components/Button';
import ErrorMessage from '../components/ErrorMessage';
import { useAuth } from '../context/AuthContext';

// Separate component for the actual login form
const LoginForm = ({ onSubmit, isSubmitting, loginError, setLoginError }) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  // Debug logging
  console.log('LoginForm: Rendering with loginError:', loginError);

  return (
    <Card>
      <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
        {loginError && (
          <ErrorMessage
            message={loginError}
            variant="error"
            onDismiss={() => setLoginError('')}
          />
        )}
        
        
        <Input
          label="Username or Email"
          {...register('username', {
            required: 'Username or email is required',
          })}
          error={errors.username?.message}
          placeholder="Enter your username or email"
          autoComplete="username"
        />
        
        <Input
          label="Password"
          type="password"
          {...register('password', {
            required: 'Password is required',
          })}
          error={errors.password?.message}
          placeholder="Enter your password"
          autoComplete="current-password"
        />
        
        <Button
          type="submit"
          className="w-full"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Signing in...' : 'Sign in'}
        </Button>
      </form>
    </Card>
  );
};

const LoginPage = () => {
  const router = useRouter();
  const { isAuthenticated, isLoading, login, clearError } = useAuth();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [loginError, setLoginError] = useState('');

  // Debug logging
  console.log('LoginPage: Current state:', { isAuthenticated, isLoading, loginError, pathname: router.pathname });

  // Redirect to tasks if user becomes authenticated
  useEffect(() => {
    if (isAuthenticated && !isLoading) {
      console.log('Login page: User authenticated, redirecting to tasks');
      router.replace('/tasks');
    }
  }, [isAuthenticated, isLoading, router]);

  const onSubmit = async (data) => {
    try {
      console.log('Login page: onSubmit called with data:', data);
      setIsSubmitting(true);
      setLoginError('');
      clearError();
      
      // Validate input before sending
      if (!data.username || !data.password) {
        setLoginError('Please enter both username and password.');
        return;
      }
      
      if (data.username.trim().length === 0 || data.password.trim().length === 0) {
        setLoginError('Username and password cannot be empty.');
        return;
      }
      
      console.log('Login page: Attempting login with:', data.username);
      console.log('Login page: Calling login function');
      
      await login({
        username: data.username.trim(),
        password: data.password
      });
      
      console.log('Login page: Login successful, redirecting to tasks');
      router.push('/tasks');
      
    } catch (error) {
      console.error('Login page: Login failed - caught error');
      console.error('Login page: Error type:', error.constructor.name);
      console.error('Login page: Error message:', error.message);
      
      // Ensure we always have a user-friendly error message
      const errorMessage = error.message || 'Login failed. Please try again.';
      console.log('Login page: Setting error message:', errorMessage);
      setLoginError(errorMessage);
      console.log('Login page: Error message set, loginError state should be:', errorMessage);
    } finally {
      console.log('Login page: Setting isSubmitting to false');
      setIsSubmitting(false);
    }
  };

  // Show loading state during initial authentication check
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // Don't render login form if user is authenticated (will redirect)
  if (isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <span className="text-xl font-bold text-gray-900">Task Manager</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/register" className="text-sm font-medium text-gray-900 hover:text-gray-700">
                Register
              </Link>
            </div>
          </div>
        </div>
      </div>
      
      {/* Login form */}
      <div className="flex-1 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
              Sign in to your account
            </h2>
            <p className="mt-2 text-center text-sm text-gray-600">
              Or{' '}
              <Link
                href="/register"
                className="font-medium create-account-link"
                style={{
                  color: 'white',
                  fontSize: '24pt',
                  fontWeight: 'bold'
                }}
              >
                create a new account
              </Link>
            </p>
          </div>
          
          <LoginForm 
            onSubmit={onSubmit}
            isSubmitting={isSubmitting}
            loginError={loginError}
            setLoginError={setLoginError}
          />
        </div>
      </div>
    </div>
  );
};

export default LoginPage;