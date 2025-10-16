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
      console.log('AuthService: Login attempt with credentials:', credentials);
      
      // Try the regular login endpoint first (sets cookies)
      const response = await apiClient.post(API_ENDPOINTS.AUTH.LOGIN, credentials);
      console.log('AuthService: Login successful, response:', response.data);
      
      // Also try the login-form endpoint to get the token in response body
      try {
        const formData = new FormData();
        formData.append('username', credentials.username);
        formData.append('password', credentials.password);
        
        const tokenResponse = await apiClient.post('/auth/login-form', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        });
        
        console.log('AuthService: Token response:', tokenResponse.data);
        
        // Store token in localStorage as backup
        if (tokenResponse.data.access_token) {
          localStorage.setItem('access_token', tokenResponse.data.access_token);
          console.log('AuthService: Token stored in localStorage');
        }
      } catch (tokenError) {
        console.warn('AuthService: Could not get token from login-form endpoint:', tokenError);
      }
      
      return response.data;
    } catch (error) {
      console.error('AuthService: Login failed, error:', error);
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
    } finally {
      // Clear token from localStorage
      localStorage.removeItem('access_token');
      console.log('AuthService: Token removed from localStorage');
    }
  }

  /**
   * Get current user information
   * @returns {Promise<Object>} Current user data
   */
  async getCurrentUser() {
    try {
      // Check if we have a token in localStorage and add it to the request
      const token = localStorage.getItem('access_token');
      if (token) {
        console.log('AuthService: Using token from localStorage for getCurrentUser');
        const response = await apiClient.get(API_ENDPOINTS.AUTH.ME, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        return response.data;
      } else {
        // Try without token (rely on cookies)
        const response = await apiClient.get(API_ENDPOINTS.AUTH.ME);
        return response.data;
      }
    } catch (error) {
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
