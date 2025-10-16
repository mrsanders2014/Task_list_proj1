import { format, formatDistanceToNow, isToday, isYesterday, isTomorrow } from 'date-fns';

/**
 * Format a date string to a readable format
 * @param {string|Date} dateString - The date to format
 * @param {string} formatString - The format string (default: 'MMM dd, yyyy')
 * @returns {string} Formatted date string
 */
export const formatDate = (dateString, formatString = 'MMM dd, yyyy') => {
  if (!dateString) return 'Not set';
  
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return 'Invalid date';
    
    return format(date, formatString);
  } catch (error) {
    return 'Invalid date';
  }
};

/**
 * Format a date to a relative time string (e.g., "2 hours ago")
 * @param {string|Date} dateString - The date to format
 * @returns {string} Relative time string
 */
export const formatRelativeTime = (dateString) => {
  if (!dateString) return 'Never';
  
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return 'Invalid date';
    
    return formatDistanceToNow(date, { addSuffix: true });
  } catch (error) {
    return 'Invalid date';
  }
};

/**
 * Format a date to a smart format (today, yesterday, tomorrow, or formatted date)
 * @param {string|Date} dateString - The date to format
 * @returns {string} Smart formatted date string
 */
export const formatSmartDate = (dateString) => {
  if (!dateString) return 'Not set';
  
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return 'Invalid date';
    
    if (isToday(date)) {
      return 'Today';
    } else if (isYesterday(date)) {
      return 'Yesterday';
    } else if (isTomorrow(date)) {
      return 'Tomorrow';
    } else {
      return format(date, 'MMM dd, yyyy');
    }
  } catch (error) {
    return 'Invalid date';
  }
};

/**
 * Check if a date is overdue
 * @param {string|Date} dateString - The date to check
 * @returns {boolean} True if the date is overdue
 */
export const isOverdue = (dateString) => {
  if (!dateString) return false;
  
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return false;
    
    return date < new Date();
  } catch (error) {
    return false;
  }
};

/**
 * Get the number of days until a date
 * @param {string|Date} dateString - The date to check
 * @returns {number} Number of days (negative if overdue)
 */
export const getDaysUntil = (dateString) => {
  if (!dateString) return null;
  
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return null;
    
    const now = new Date();
    const diffTime = date.getTime() - now.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    return diffDays;
  } catch (error) {
    return null;
  }
};

export default {
  formatDate,
  formatRelativeTime,
  formatSmartDate,
  isOverdue,
  getDaysUntil,
};
