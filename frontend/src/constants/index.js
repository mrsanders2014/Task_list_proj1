// Task status constants
export const TASK_STATUS = {
  CREATED: 'Created',
  STARTED: 'Started',
  IN_PROCESS: 'InProcess',
  MODIFIED: 'Modified',
  SCHEDULED: 'Scheduled',
  COMPLETE: 'Complete',
  DELETED: 'Deleted',
};

// Task status options for forms
export const TASK_STATUS_OPTIONS = [
  { value: TASK_STATUS.CREATED, label: 'Created', color: 'bg-gray-500' },
  { value: TASK_STATUS.STARTED, label: 'Started', color: 'bg-blue-500' },
  { value: TASK_STATUS.IN_PROCESS, label: 'In Process', color: 'bg-yellow-500' },
  { value: TASK_STATUS.MODIFIED, label: 'Modified', color: 'bg-orange-500' },
  { value: TASK_STATUS.SCHEDULED, label: 'Scheduled', color: 'bg-purple-500' },
  { value: TASK_STATUS.COMPLETE, label: 'Complete', color: 'bg-green-500' },
  { value: TASK_STATUS.DELETED, label: 'Deleted', color: 'bg-red-500' },
];

// Priority levels
export const PRIORITY_LEVELS = {
  LOW: 1,
  MEDIUM_LOW: 3,
  MEDIUM: 5,
  MEDIUM_HIGH: 7,
  HIGH: 9,
  CRITICAL: 10,
};

// Priority options for forms
export const PRIORITY_OPTIONS = [
  { value: PRIORITY_LEVELS.LOW, label: 'Low (1)', color: 'bg-green-100 text-green-800' },
  { value: PRIORITY_LEVELS.MEDIUM_LOW, label: 'Medium Low (3)', color: 'bg-blue-100 text-blue-800' },
  { value: PRIORITY_LEVELS.MEDIUM, label: 'Medium (5)', color: 'bg-yellow-100 text-yellow-800' },
  { value: PRIORITY_LEVELS.MEDIUM_HIGH, label: 'Medium High (7)', color: 'bg-orange-100 text-orange-800' },
  { value: PRIORITY_LEVELS.HIGH, label: 'High (9)', color: 'bg-red-100 text-red-800' },
  { value: PRIORITY_LEVELS.CRITICAL, label: 'Critical (10)', color: 'bg-red-200 text-red-900' },
];

// Time units for estimated time
export const TIME_UNITS = [
  { value: 'minutes', label: 'Minutes' },
  { value: 'hours', label: 'Hours' },
  { value: 'days', label: 'Days' },
  { value: 'weeks', label: 'Weeks' },
  { value: 'months', label: 'Months' },
  { value: 'years', label: 'Years' },
];

// Default label colors
export const LABEL_COLORS = [
  '#808080', // Gray
  '#FF6B6B', // Red
  '#4ECDC4', // Teal
  '#45B7D1', // Blue
  '#96CEB4', // Green
  '#FFEAA7', // Yellow
  '#DDA0DD', // Plum
  '#98D8C8', // Mint
  '#F7DC6F', // Light Yellow
  '#BB8FCE', // Light Purple
];

// API endpoints
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    LOGOUT: '/auth/logout',
    ME: '/auth/me',
    REFRESH: '/auth/refresh',
  },
  TASKS: {
    LIST: '/tasks',
    CREATE: '/tasks',
    DETAIL: (id) => `/tasks/${id}`,
    UPDATE: (id) => `/tasks/${id}`,
    DELETE: (id) => `/tasks/${id}`,
    STATUS_UPDATE: (id) => `/tasks/${id}/status`,
    STATISTICS: '/tasks/statistics/overview',
    USER_TASKS: (userId) => `/tasks/user/${userId}`,
  },
  USERS: {
    LIST: '/users',
    CREATE: '/users',
    DETAIL: (id) => `/users/${id}`,
    UPDATE: (id) => `/users/${id}`,
    DELETE: (id) => `/users/${id}`,
    STATUS_UPDATE: (id) => `/users/${id}/status`,
    BY_USERNAME: (username) => `/users/username/${username}`,
    BY_EMAIL: (email) => `/users/email/${email}`,
  },
};

// Form validation rules
export const VALIDATION_RULES = {
  USERNAME: {
    MIN_LENGTH: 3,
    MAX_LENGTH: 50,
  },
  PASSWORD: {
    MIN_LENGTH: 6,
  },
  TASK_TITLE: {
    MIN_LENGTH: 1,
    MAX_LENGTH: 50,
  },
  TASK_DESCRIPTION: {
    MAX_LENGTH: 250,
  },
  EMAIL: {
    PATTERN: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  },
};

// Pagination defaults
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 10,
  MAX_PAGE_SIZE: 100,
  PAGE_SIZE_OPTIONS: [10, 25, 50, 100],
};
