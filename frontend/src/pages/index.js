import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { useForm } from 'react-hook-form';
import Card from '../components/Card';
import Input from '../components/Input';
import Button from '../components/Button';
import ErrorMessage from '../components/ErrorMessage';
import apiClient from '../config/api';

// Separate component for the actual login form
const LoginForm = ({ onSubmit, isSubmitting, loginError, setLoginError }) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  return (
    <Card>
      <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
        {loginError && (
          <ErrorMessage
            message={loginError}
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
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [loginError, setLoginError] = useState('');

  // Check if user is already authenticated on page load
  useEffect(() => {
    const checkAuth = () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        console.log('Login page: Token found, redirecting to tasks');
        router.push('/tasks');
      }
    };
    
    // Small delay to prevent immediate redirects
    const timer = setTimeout(checkAuth, 100);
    return () => clearTimeout(timer);
  }, [router]);

  const onSubmit = async (data) => {
    try {
      setIsSubmitting(true);
      setLoginError('');
      
      console.log('Login page: Attempting login with:', data.username);
      
      // Call login endpoint directly
      const response = await apiClient.post('/auth/login', {
        username: data.username,
        password: data.password
      });
      
      console.log('Login page: Login response:', response.data);
      
      // Also get token from login-form endpoint
      try {
        const formData = new FormData();
        formData.append('username', data.username);
        formData.append('password', data.password);
        
        const tokenResponse = await apiClient.post('/auth/login-form', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        });
        
        if (tokenResponse.data.access_token) {
          localStorage.setItem('access_token', tokenResponse.data.access_token);
          console.log('Login page: Token stored in localStorage');
        }
      } catch (tokenError) {
        console.warn('Login page: Could not get token:', tokenError);
      }
      
      // Redirect to tasks page
      router.push('/tasks');
      
    } catch (error) {
      console.error('Login page: Login failed:', error);
      let errorMessage = 'Login failed';
      
      if (error.response?.data?.detail) {
        if (typeof error.response.data.detail === 'string') {
          errorMessage = error.response.data.detail;
        } else if (Array.isArray(error.response.data.detail)) {
          errorMessage = error.response.data.detail.map(err => err.msg).join(', ');
        }
      } else if (error.response?.data?.message) {
        errorMessage = error.response.data.message;
      }
      
      setLoginError(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  // No loading screen - show form immediately

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Minimal header without AuthContext */}
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
                className="font-medium text-gray-900 hover:text-gray-700"
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
