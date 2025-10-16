/**
 * Validation utility functions
 */

/**
 * Validate email address
 * @param {string} email - Email to validate
 * @returns {boolean} True if valid email
 */
export const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * Validate password strength
 * @param {string} password - Password to validate
 * @returns {Object} Validation result with isValid and message
 */
export const validatePassword = (password) => {
  if (!password) {
    return { isValid: false, message: 'Password is required' };
  }
  
  if (password.length < 6) {
    return { isValid: false, message: 'Password must be at least 6 characters long' };
  }
  
  return { isValid: true, message: 'Password is valid' };
};

/**
 * Validate username
 * @param {string} username - Username to validate
 * @returns {Object} Validation result with isValid and message
 */
export const validateUsername = (username) => {
  if (!username) {
    return { isValid: false, message: 'Username is required' };
  }
  
  if (username.length < 3) {
    return { isValid: false, message: 'Username must be at least 3 characters long' };
  }
  
  if (username.length > 50) {
    return { isValid: false, message: 'Username must be less than 50 characters' };
  }
  
  const usernameRegex = /^[a-zA-Z0-9_-]+$/;
  if (!usernameRegex.test(username)) {
    return { isValid: false, message: 'Username can only contain letters, numbers, underscores, and hyphens' };
  }
  
  return { isValid: true, message: 'Username is valid' };
};

/**
 * Validate task title
 * @param {string} title - Task title to validate
 * @returns {Object} Validation result with isValid and message
 */
export const validateTaskTitle = (title) => {
  if (!title) {
    return { isValid: false, message: 'Task title is required' };
  }
  
  if (title.length < 1) {
    return { isValid: false, message: 'Task title cannot be empty' };
  }
  
  if (title.length > 50) {
    return { isValid: false, message: 'Task title must be less than 50 characters' };
  }
  
  return { isValid: true, message: 'Task title is valid' };
};

/**
 * Validate task description
 * @param {string} description - Task description to validate
 * @returns {Object} Validation result with isValid and message
 */
export const validateTaskDescription = (description) => {
  if (description && description.length > 250) {
    return { isValid: false, message: 'Task description must be less than 250 characters' };
  }
  
  return { isValid: true, message: 'Task description is valid' };
};

/**
 * Validate priority level
 * @param {number} priority - Priority level to validate
 * @returns {Object} Validation result with isValid and message
 */
export const validatePriority = (priority) => {
  if (priority === undefined || priority === null) {
    return { isValid: true, message: 'Priority is optional' };
  }
  
  const numPriority = Number(priority);
  
  if (isNaN(numPriority)) {
    return { isValid: false, message: 'Priority must be a number' };
  }
  
  if (numPriority < 1 || numPriority > 10) {
    return { isValid: false, message: 'Priority must be between 1 and 10' };
  }
  
  return { isValid: true, message: 'Priority is valid' };
};

/**
 * Validate estimated time
 * @param {number} time - Estimated time to validate
 * @returns {Object} Validation result with isValid and message
 */
export const validateEstimatedTime = (time) => {
  if (time === undefined || time === null || time === '') {
    return { isValid: true, message: 'Estimated time is optional' };
  }
  
  const numTime = Number(time);
  
  if (isNaN(numTime)) {
    return { isValid: false, message: 'Estimated time must be a number' };
  }
  
  if (numTime < 0) {
    return { isValid: false, message: 'Estimated time cannot be negative' };
  }
  
  return { isValid: true, message: 'Estimated time is valid' };
};

/**
 * Validate form data
 * @param {Object} data - Form data to validate
 * @param {Object} rules - Validation rules
 * @returns {Object} Validation result with isValid and errors
 */
export const validateForm = (data, rules) => {
  const errors = {};
  let isValid = true;
  
  Object.keys(rules).forEach(field => {
    const value = data[field];
    const rule = rules[field];
    
    if (rule.required && (!value || value.toString().trim() === '')) {
      errors[field] = rule.message || `${field} is required`;
      isValid = false;
    } else if (value && rule.validator) {
      const result = rule.validator(value);
      if (!result.isValid) {
        errors[field] = result.message;
        isValid = false;
      }
    }
  });
  
  return { isValid, errors };
};

export default {
  isValidEmail,
  validatePassword,
  validateUsername,
  validateTaskTitle,
  validateTaskDescription,
  validatePriority,
  validateEstimatedTime,
  validateForm,
};
