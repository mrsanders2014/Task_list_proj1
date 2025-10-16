import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

// Debug: Log the API configuration
console.log('API Configuration:', {
  NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  API_BASE_URL: API_BASE_URL,
  NODE_ENV: process.env.NODE_ENV
});

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Enable cookies for HTTP-only JWT tokens
  timeout: 10000, // 10 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Connectivity test removed to prevent resource exhaustion

// Request interceptor for logging and adding common headers
apiClient.interceptors.request.use(
  (config) => {
    // Reduced logging to prevent performance issues
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors and token refresh
apiClient.interceptors.response.use(
  (response) => {
    // Reduced logging to prevent performance issues
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    
    // Reduced logging to prevent performance issues
    console.error('Response error:', error.response?.status, error.config?.url);

    // Handle 401 errors (unauthorized)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      // Don't try to refresh if the original request was already a refresh request
      if (originalRequest.url?.includes('/auth/refresh')) {
        console.log('Refresh token request failed, redirecting to login');
        if (typeof window !== 'undefined') {
          window.location.href = '/'; // Redirect to home page where login form is located
        }
        return Promise.reject(error);
      }

      // Don't try to refresh if the original request was /auth/me (to prevent loops)
      if (originalRequest.url?.includes('/auth/me')) {
        console.log('Auth check failed, redirecting to login');
        if (typeof window !== 'undefined') {
          window.location.href = '/'; // Redirect to home page where login form is located
        }
        return Promise.reject(error);
      }

      try {
        console.log('Attempting to refresh token...');
        // Attempt to refresh token
        await apiClient.post('/auth/refresh');
        console.log('Token refreshed successfully, retrying original request');
        // Retry the original request
        return apiClient(originalRequest);
      } catch (refreshError) {
        console.error('Token refresh failed:', refreshError);
        // Refresh failed, redirect to login
        if (typeof window !== 'undefined') {
          window.location.href = '/'; // Redirect to home page where login form is located
        }
        return Promise.reject(refreshError);
      }
    }

    // Handle other errors
    return Promise.reject(error);
  }
);

export default apiClient;
