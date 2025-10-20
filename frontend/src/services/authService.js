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
    try {
      // Use the regular login endpoint (sets httpOnly cookies)
      const response = await apiClient.post(API_ENDPOINTS.AUTH.LOGIN, credentials);
      return response.data;
    } catch (error) {
      // Handle specific HTTP error status codes
      const status = error.response?.status;
      
      if (status === 401) {
        const errorMsg = 'Invalid username or password. Please check your credentials and try again.';
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
    }
  }

  /**
   * Get current user information
   * @returns {Promise<Object>} Current user data
   */
  async getCurrentUser() {
    try {
      const response = await apiClient.get(API_ENDPOINTS.AUTH.ME);
      return response.data;
    } catch (error) {
      // Handle timeout errors specifically
      if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
        const timeoutError = new Error('Request timeout. Please check your connection and try again.');
        timeoutError.code = 'TIMEOUT';
        throw timeoutError;
      }
      
      // Handle 401 errors gracefully (user not authenticated)
      if (error.response?.status === 401) {
        // Don't try to refresh token here as it might cause infinite loops
        // The calling code should handle token refresh if needed
        throw this.handleError(error);
      }
      
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
      // If we get a 401, try to refresh the token
      if (error.response?.status === 401) {
        try {
          await this.refreshToken();
          // Try again after refresh
          await this.getCurrentUser();
          return true;
        } catch (refreshError) {
          return false;
        }
      }
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
      
      // Handle specific error cases with user-friendly messages
      if (status === 409) {
        if (data?.detail && data.detail.includes('username')) {
          message = 'A user with this username already exists. Please choose a different username.';
        } else if (data?.detail && data.detail.includes('email')) {
          message = 'A user with this email already exists. Please use a different email address.';
        } else {
          message = 'This information is already in use. Please check your details and try again.';
        }
      } else if (status === 400) {
        if (data?.detail) {
          if (Array.isArray(data.detail)) {
            // Handle validation errors
            message = data.detail.map(err => {
              const field = err.loc?.join('.') || 'field';
              return `${field}: ${err.msg}`;
            }).join(', ');
          } else if (typeof data.detail === 'string') {
            message = data.detail;
          }
        } else {
          message = 'Please check your information and try again.';
        }
      } else if (status === 422) {
        message = 'Please check your information and try again.';
      } else if (status >= 500) {
        message = 'Server error. Please try again later.';
      } else {
        // Handle other error formats
        if (typeof data === 'string') {
          message = data;
        } else if (data?.detail) {
          if (typeof data.detail === 'string') {
            message = data.detail;
          } else if (Array.isArray(data.detail)) {
            message = data.detail.map(err => `${err.loc?.join('.')}: ${err.msg}`).join(', ');
          } else {
            message = JSON.stringify(data.detail);
          }
        } else if (data?.message) {
          message = data.message;
        } else if (data) {
          message = JSON.stringify(data);
        }
      }
      
      return new Error(message);
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