import apiClient from '../config/api';
import { API_ENDPOINTS } from '../constants';

class UserService {
  /**
   * Get all users with optional filtering
   * @param {Object} filters - Filter options
   * @returns {Promise<Array>} List of users
   */
  async getUsers(filters = {}) {
    try {
      const params = new URLSearchParams();
      
      // Add filter parameters
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          params.append(key, value);
        }
      });

      const response = await apiClient.get(`${API_ENDPOINTS.USERS.LIST}?${params}`);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Get a specific user by ID
   * @param {string} userId - User ID
   * @returns {Promise<Object>} User data
   */
  async getUser(userId) {
    try {
      const response = await apiClient.get(API_ENDPOINTS.USERS.DETAIL(userId));
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Create a new user
   * @param {Object} userData - User creation data
   * @returns {Promise<Object>} Created user data
   */
  async createUser(userData) {
    try {
      const response = await apiClient.post(API_ENDPOINTS.USERS.CREATE, userData);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Update an existing user
   * @param {string} userId - User ID
   * @param {Object} userData - User update data
   * @returns {Promise<Object>} Updated user data
   */
  async updateUser(userId, userData) {
    try {
      const response = await apiClient.put(API_ENDPOINTS.USERS.UPDATE(userId), userData);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Delete a user
   * @param {string} userId - User ID
   * @returns {Promise<void>}
   */
  async deleteUser(userId) {
    try {
      await apiClient.delete(API_ENDPOINTS.USERS.DELETE(userId));
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Update user status (activate/deactivate)
   * @param {string} userId - User ID
   * @param {boolean} isActive - New active status
   * @returns {Promise<Object>} Updated user data
   */
  async updateUserStatus(userId, isActive) {
    try {
      const response = await apiClient.patch(
        API_ENDPOINTS.USERS.STATUS_UPDATE(userId),
        null,
        { params: { is_active: isActive } }
      );
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Get user by username
   * @param {string} username - Username
   * @returns {Promise<Object>} User data
   */
  async getUserByUsername(username) {
    try {
      const response = await apiClient.get(API_ENDPOINTS.USERS.BY_USERNAME(username));
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Get user by email
   * @param {string} email - Email address
   * @returns {Promise<Object>} User data
   */
  async getUserByEmail(email) {
    try {
      const response = await apiClient.get(API_ENDPOINTS.USERS.BY_EMAIL(email));
      return response.data;
    } catch (error) {
      throw this.handleError(error);
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
      const message = data?.detail || data?.message || 'An error occurred';
      
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

export default new UserService();
