import axios from 'axios';

// Get API base URL from environment or use default
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

console.log('API Configuration:', {
  NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  API_BASE_URL,
  NODE_ENV: process.env.NODE_ENV
});

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 5000, // Reduced timeout to 5 seconds
  withCredentials: true, // Important: This allows cookies to be sent with requests
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle 401 errors gracefully (user not authenticated)
    if (error.response?.status === 401) {
      console.log('API: User not authenticated (401) - this is normal');
    } else if (error.response?.status >= 400) {
      // Log client errors (4xx) and server errors (5xx) for debugging
      console.log('API Error:', error.response?.status, error.response?.data);
    } else if (!error.response) {
      // Network error
      console.log('API: Network error - no response received');
    }
    
    // Always reject the promise to allow proper error handling in components
    return Promise.reject(error);
  }
);

export default apiClient;