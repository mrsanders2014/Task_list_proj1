import apiClient from '../config/api';
import { API_ENDPOINTS } from '../constants';

class AuthService {
  /**
   * Register a new user
   * @param {Object} userData - User registration data
   * @returns {Promise<Object>} User data
   */
  async register(userData) {
    try {
      const response = await apiClient.post(API_ENDPOINTS.AUTH.REGISTER, userData);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Login user
   * @param {Object} credentials - Login credentials
   * @returns {Promise<Object>} User data
   */
  async login(credentials) {
    console.log('AuthService: Login attempt with credentials:', credentials.username);
    
    try {
      // Use the regular login endpoint (sets httpOnly cookies)
      console.log('AuthService: Making POST request to:', API_ENDPOINTS.AUTH.LOGIN);
      const response = await apiClient.post(API_ENDPOINTS.AUTH.LOGIN, credentials);
      console.log('AuthService: Login successful');
      return response.data;
    } catch (error) {
      console.error('AuthService: Login failed - caught error');
      console.error('AuthService: Error type:', error.constructor.name);
      console.error('AuthService: Error status:', error.response?.status);
      console.error('AuthService: Error data:', error.response?.data);
      
      // Handle specific HTTP error status codes
      const status = error.response?.status;
      
      if (status === 401) {
        const errorMsg = 'Invalid username or password. Please check your credentials and try again.';
        console.log('AuthService: Converting 401 to user-friendly error');
        const friendlyError = new Error(errorMsg);
        friendlyError.status = 401;
        throw friendlyError;
      }
      
      if (status === 422) {
        throw new Error('Please check your input. Username and password are required.');
      }
      
      if (status === 429) {
        throw new Error('Too many login attempts. Please wait a moment and try again.');
      }
      
      if (status >= 500) {
        throw new Error('Server error. Please try again later.');
      }
      
      if (!error.response) {
        throw new Error('Unable to connect to server. Please check your internet connection.');
      }
      
      // Default error handling
      console.log('AuthService: Using default error handler');
      throw this.handleError(error);
    }
  }

  /**
   * Logout user
   * @returns {Promise<void>}
   */
  async logout() {
    try {
      await apiClient.post(API_ENDPOINTS.AUTH.LOGOUT);
    } catch (error) {
      // Even if logout fails on server, we should clear local state
      console.warn('Logout request failed:', error);
    }
  }

  /**
   * Get current user information
   * @returns {Promise<Object>} Current user data
   */
  async getCurrentUser() {
    try {
      console.log('AuthService: Getting current user...');
      console.log('AuthService: Making request to:', API_ENDPOINTS.AUTH.ME);
      const response = await apiClient.get(API_ENDPOINTS.AUTH.ME);
      console.log('AuthService: Current user retrieved:', response.data.username);
      return response.data;
    } catch (error) {
      // Handle 401 errors gracefully (user not authenticated)
      if (error.response?.status === 401) {
        console.log('AuthService: User not authenticated (401) - this is normal');
        throw this.handleError(error);
      }
      
      console.error('AuthService: Error in getCurrentUser:', error);
      console.error('AuthService: Error response:', error.response?.data);
      console.error('AuthService: Error status:', error.response?.status);
      throw this.handleError(error);
    }
  }

  /**
   * Refresh authentication token
   * @returns {Promise<Object>} New token data
   */
  async refreshToken() {
    try {
      const response = await apiClient.post(API_ENDPOINTS.AUTH.REFRESH);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Check if user is authenticated
   * @returns {Promise<boolean>} Authentication status
   */
  async isAuthenticated() {
    try {
      await this.getCurrentUser();
      return true;
    } catch (error) {
      return false;
    }
  }

  /**
   * Handle API errors
   * @param {Error} error - API error
   * @returns {Error} Formatted error
   */
  handleError(error) {
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;
      console.error('AuthService: API Error Response:', { status, data });
      
      let message = 'An error occurred';
      
      if (typeof data === 'string') {
        message = data;
      } else if (data?.detail) {
        if (typeof data.detail === 'string') {
          message = data.detail;
        } else if (Array.isArray(data.detail)) {
          // Handle validation errors
          message = data.detail.map(err => `${err.loc?.join('.')}: ${err.msg}`).join(', ');
        } else {
          message = JSON.stringify(data.detail);
        }
      } else if (data?.message) {
        message = data.message;
      } else if (data) {
        message = JSON.stringify(data);
      }
      
      return new Error(`${status}: ${message}`);
    } else if (error.request) {
      // Request was made but no response received
      return new Error('Network error: Unable to connect to server');
    } else {
      // Something else happened
      return new Error(error.message || 'An unexpected error occurred');
    }
  }
}

export default new AuthService();