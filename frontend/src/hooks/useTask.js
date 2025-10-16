import { useContext } from 'react';
import TaskContext from '../context/TaskContext';

/**
 * Custom hook to access task context
 * @returns {Object} Task state and methods
 */
export const useTask = () => {
  const context = useContext(TaskContext);
  
  if (!context) {
    throw new Error('useTask must be used within a TaskProvider');
  }
  
  return context;
};

export default useTask;
