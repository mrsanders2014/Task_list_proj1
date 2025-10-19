import React, { createContext, useContext, useReducer, useEffect, useCallback, useRef } from 'react';
import taskService from '../services/taskService';
import { useAuth } from './AuthContext';

// Initial state
const initialState = {
  tasks: [],
  currentTask: null,
  statistics: null,
  isLoading: false,
  error: null,
  filters: {
    task_status: '',
    min_priority: '',
    max_priority: '',
    label_name: '',
    overdue_only: false,
    skip: 0,
    limit: 10,
  },
  pagination: {
    currentPage: 1,
    totalPages: 1,
    totalItems: 0,
    pageSize: 10,
  },
};

// Action types
const TASK_ACTIONS = {
  SET_LOADING: 'SET_LOADING',
  SET_ERROR: 'SET_ERROR',
  CLEAR_ERROR: 'CLEAR_ERROR',
  SET_TASKS: 'SET_TASKS',
  ADD_TASK: 'ADD_TASK',
  UPDATE_TASK: 'UPDATE_TASK',
  DELETE_TASK: 'DELETE_TASK',
  SET_CURRENT_TASK: 'SET_CURRENT_TASK',
  CLEAR_CURRENT_TASK: 'CLEAR_CURRENT_TASK',
  SET_STATISTICS: 'SET_STATISTICS',
  SET_FILTERS: 'SET_FILTERS',
  SET_PAGINATION: 'SET_PAGINATION',
  RESET_FILTERS: 'RESET_FILTERS',
};

// Reducer
const taskReducer = (state, action) => {
  switch (action.type) {
    case TASK_ACTIONS.SET_LOADING:
      return {
        ...state,
        isLoading: action.payload,
      };
    case TASK_ACTIONS.SET_ERROR:
      return {
        ...state,
        error: action.payload,
        isLoading: false,
      };
    case TASK_ACTIONS.CLEAR_ERROR:
      return {
        ...state,
        error: null,
      };
    case TASK_ACTIONS.SET_TASKS:
      return {
        ...state,
        tasks: action.payload,
        isLoading: false,
        error: null,
      };
    case TASK_ACTIONS.ADD_TASK:
      return {
        ...state,
        tasks: [action.payload, ...state.tasks],
        isLoading: false,
        error: null,
      };
    case TASK_ACTIONS.UPDATE_TASK:
      return {
        ...state,
        tasks: state.tasks.map(task =>
          task.id === action.payload.id ? action.payload : task
        ),
        currentTask: state.currentTask?.id === action.payload.id ? action.payload : state.currentTask,
        isLoading: false,
        error: null,
      };
    case TASK_ACTIONS.DELETE_TASK:
      return {
        ...state,
        tasks: state.tasks.filter(task => task.id !== action.payload),
        currentTask: state.currentTask?.id === action.payload ? null : state.currentTask,
        isLoading: false,
        error: null,
      };
    case TASK_ACTIONS.SET_CURRENT_TASK:
      return {
        ...state,
        currentTask: action.payload,
        isLoading: false,
        error: null,
      };
    case TASK_ACTIONS.CLEAR_CURRENT_TASK:
      return {
        ...state,
        currentTask: null,
      };
    case TASK_ACTIONS.SET_STATISTICS:
      return {
        ...state,
        statistics: action.payload,
        isLoading: false,
        error: null,
      };
    case TASK_ACTIONS.SET_FILTERS:
      return {
        ...state,
        filters: { ...state.filters, ...action.payload },
      };
    case TASK_ACTIONS.SET_PAGINATION:
      return {
        ...state,
        pagination: { ...state.pagination, ...action.payload },
      };
    case TASK_ACTIONS.RESET_FILTERS:
      return {
        ...state,
        filters: initialState.filters,
        pagination: initialState.pagination,
      };
    default:
      return state;
  }
};

// Create context
const TaskContext = createContext();

// Task provider component
export const TaskProvider = ({ children }) => {
  const [state, dispatch] = useReducer(taskReducer, initialState);
  const lastFetchTime = useRef(0);
  const FETCH_COOLDOWN = 1000; // 1 second cooldown between requests
  const { user } = useAuth();

  const setLoading = useCallback((loading) => {
    dispatch({ type: TASK_ACTIONS.SET_LOADING, payload: loading });
  }, []);

  const setError = useCallback((error) => {
    dispatch({ type: TASK_ACTIONS.SET_ERROR, payload: error });
  }, []);

  const clearError = useCallback(() => {
    dispatch({ type: TASK_ACTIONS.CLEAR_ERROR });
  }, []);

  const fetchTasks = useCallback(async (customFilters = {}, forceRefresh = false) => {
    console.log('TaskContext: fetchTasks called with:', { customFilters, forceRefresh });
    const now = Date.now();
    if (!forceRefresh && now - lastFetchTime.current < FETCH_COOLDOWN) {
      console.log('TaskContext: Rate limiting: skipping fetch tasks request');
      return state.tasks; // Return cached data
    }
    
    try {
      console.log('TaskContext: Setting loading to true for tasks');
      setLoading(true);
      lastFetchTime.current = now;
      const filters = { ...state.filters, ...customFilters };
      console.log('TaskContext: Fetching tasks with filters:', filters);
      console.log('TaskContext: About to call taskService.getTasks...');
      const tasks = await taskService.getTasks(filters);
      console.log('TaskContext: Tasks fetched successfully:', tasks.length, tasks);
      dispatch({ type: TASK_ACTIONS.SET_TASKS, payload: tasks });
      return tasks;
    } catch (error) {
      console.error('TaskContext: Error fetching tasks:', error);
      console.error('TaskContext: Error details:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status
      });
      setError(error.message);
      // Don't throw the error to prevent the app from crashing
      // Return empty array as fallback
      return [];
    } finally {
      console.log('TaskContext: Setting loading to false for tasks');
      setLoading(false);
    }
  }, []); // Remove all dependencies to prevent infinite re-renders

  const fetchTask = useCallback(async (taskId) => {
    try {
      console.log('TaskContext: fetchTask called with taskId:', taskId);
      setLoading(true);
      const task = await taskService.getTask(taskId);
      console.log('TaskContext: fetchTask successful, task:', task);
      dispatch({ type: TASK_ACTIONS.SET_CURRENT_TASK, payload: task });
      return task;
    } catch (error) {
      console.error('TaskContext: Error in fetchTask:', error);
      setError(error.message);
      throw error;
    }
  }, []); // Empty dependency array since this function doesn't depend on any state

  const createTask = useCallback(async (taskData) => {
    try {
      setLoading(true);
      const newTask = await taskService.createTask(taskData);
      dispatch({ type: TASK_ACTIONS.ADD_TASK, payload: newTask });
      return newTask;
    } catch (error) {
      setError(error.message);
      throw error;
    }
  }, []);

  const updateTask = useCallback(async (taskId, taskData) => {
    try {
      setLoading(true);
      const updatedTask = await taskService.updateTask(taskId, taskData);
      dispatch({ type: TASK_ACTIONS.UPDATE_TASK, payload: updatedTask });
      return updatedTask;
    } catch (error) {
      setError(error.message);
      throw error;
    }
  }, []);

  const deleteTask = useCallback(async (taskId) => {
    try {
      setLoading(true);
      await taskService.deleteTask(taskId);
      dispatch({ type: TASK_ACTIONS.DELETE_TASK, payload: taskId });
    } catch (error) {
      setError(error.message);
      throw error;
    }
  }, []);

  const updateTaskStatus = useCallback(async (taskId, status, reason = '') => {
    try {
      setLoading(true);
      const updatedTask = await taskService.updateTaskStatus(taskId, status, reason);
      dispatch({ type: TASK_ACTIONS.UPDATE_TASK, payload: updatedTask });
      return updatedTask;
    } catch (error) {
      setError(error.message);
      throw error;
    }
  }, []);

  const fetchStatistics = useCallback(async () => {
    console.log('TaskContext: fetchStatistics called');
    const now = Date.now();
    if (now - lastFetchTime.current < FETCH_COOLDOWN) {
      console.log('TaskContext: Rate limiting: skipping fetch request');
      return state.statistics; // Return cached data
    }
    
    try {
      console.log('TaskContext: Setting loading to true for statistics');
      setLoading(true);
      lastFetchTime.current = now;
      console.log('TaskContext: About to call taskService.getTaskStatistics()');
      const statistics = await taskService.getTaskStatistics();
      console.log('TaskContext: Statistics fetched successfully:', statistics);
      dispatch({ type: TASK_ACTIONS.SET_STATISTICS, payload: statistics });
      return statistics;
    } catch (error) {
      console.error('TaskContext: Error fetching statistics:', error);
      setError(error.message);
      // Don't throw the error to prevent the app from crashing
      // Return null as fallback
      return null;
    } finally {
      console.log('TaskContext: Setting loading to false for statistics');
      setLoading(false);
    }
  }, []); // Remove state.statistics dependency to prevent unnecessary re-renders

  const setFilters = useCallback((filters) => {
    dispatch({ type: TASK_ACTIONS.SET_FILTERS, payload: filters });
  }, []);

  const setPagination = useCallback((pagination) => {
    dispatch({ type: TASK_ACTIONS.SET_PAGINATION, payload: pagination });
  }, []);

  const resetFilters = useCallback(() => {
    dispatch({ type: TASK_ACTIONS.RESET_FILTERS });
  }, []);

  const clearCurrentTask = useCallback(() => {
    dispatch({ type: TASK_ACTIONS.CLEAR_CURRENT_TASK });
  }, []);

  // Clear tasks and statistics when user changes
  useEffect(() => {
    if (user?.username) {
      // Clear current task when user changes
      dispatch({ type: TASK_ACTIONS.CLEAR_CURRENT_TASK });
      // Reset tasks and statistics to prevent stale data
      dispatch({ type: TASK_ACTIONS.SET_TASKS, payload: [] });
      dispatch({ type: TASK_ACTIONS.SET_STATISTICS, payload: null });
    }
  }, [user?.username]);

  const value = {
    ...state,
    fetchTasks,
    fetchTask,
    createTask,
    updateTask,
    deleteTask,
    updateTaskStatus,
    fetchStatistics,
    setFilters,
    setPagination,
    resetFilters,
    clearCurrentTask,
    setError,
    clearError,
  };

  return (
    <TaskContext.Provider value={value}>
      {children}
    </TaskContext.Provider>
  );
};

// Custom hook to use task context
export const useTask = () => {
  const context = useContext(TaskContext);
  if (!context) {
    throw new Error('useTask must be used within a TaskProvider');
  }
  return context;
};

export default TaskContext;
