import apiClient from '../config/api';
import { API_ENDPOINTS } from '../constants';

class TaskService {
  /**
   * Get all tasks with optional filtering
   * @param {Object} filters - Filter options
   * @returns {Promise<Array>} List of tasks
   */
  async getTasks(filters = {}) {
    try {
      const params = new URLSearchParams();
      
      // Add filter parameters
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          params.append(key, value);
        }
      });

      const response = await apiClient.get(`${API_ENDPOINTS.TASKS.LIST}?${params}`);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Get a specific task by ID
   * @param {string} taskId - Task ID
   * @returns {Promise<Object>} Task data
   */
  async getTask(taskId) {
    try {
      const response = await apiClient.get(API_ENDPOINTS.TASKS.DETAIL(taskId));
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Create a new task
   * @param {Object} taskData - Task creation data
   * @returns {Promise<Object>} Created task data
   */
  async createTask(taskData) {
    try {
      const response = await apiClient.post(API_ENDPOINTS.TASKS.CREATE, taskData);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Update an existing task
   * @param {string} taskId - Task ID
   * @param {Object} taskData - Task update data
   * @returns {Promise<Object>} Updated task data
   */
  async updateTask(taskId, taskData) {
    try {
      const response = await apiClient.put(API_ENDPOINTS.TASKS.UPDATE(taskId), taskData);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Delete a task
   * @param {string} taskId - Task ID
   * @returns {Promise<void>}
   */
  async deleteTask(taskId) {
    try {
      await apiClient.delete(API_ENDPOINTS.TASKS.DELETE(taskId));
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Update task status
   * @param {string} taskId - Task ID
   * @param {string} status - New status
   * @param {string} reason - Reason for status change
   * @returns {Promise<Object>} Updated task data
   */
  async updateTaskStatus(taskId, status, reason = '') {
    try {
      const response = await apiClient.patch(
        API_ENDPOINTS.TASKS.STATUS_UPDATE(taskId),
        { status, reason }
      );
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Get task statistics
   * @returns {Promise<Object>} Task statistics
   */
  async getTaskStatistics() {
    try {
      const response = await apiClient.get(API_ENDPOINTS.TASKS.STATISTICS);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Get tasks for a specific user
   * @param {string} userId - User ID
   * @param {Object} filters - Additional filters
   * @returns {Promise<Array>} User's tasks
   */
  async getUserTasks(userId, filters = {}) {
    try {
      const params = new URLSearchParams();
      
      // Add filter parameters
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          params.append(key, value);
        }
      });

      const response = await apiClient.get(
        `${API_ENDPOINTS.TASKS.USER_TASKS(userId)}?${params}`
      );
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

export default new TaskService();
