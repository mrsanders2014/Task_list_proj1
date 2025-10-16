import React, { createContext, useContext, useReducer, useEffect, useCallback, useRef } from 'react';
import taskService from '../services/taskService';

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

  const setLoading = (loading) => {
    dispatch({ type: TASK_ACTIONS.SET_LOADING, payload: loading });
  };

  const setError = (error) => {
    dispatch({ type: TASK_ACTIONS.SET_ERROR, payload: error });
  };

  const clearError = () => {
    dispatch({ type: TASK_ACTIONS.CLEAR_ERROR });
  };

  const fetchTasks = async (customFilters = {}) => {
    const now = Date.now();
    if (now - lastFetchTime.current < FETCH_COOLDOWN) {
      console.log('Rate limiting: skipping fetch tasks request');
      return state.tasks; // Return cached data
    }
    
    try {
      setLoading(true);
      lastFetchTime.current = now;
      const filters = { ...state.filters, ...customFilters };
      const tasks = await taskService.getTasks(filters);
      dispatch({ type: TASK_ACTIONS.SET_TASKS, payload: tasks });
      return tasks;
    } catch (error) {
      setError(error.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const fetchTask = async (taskId) => {
    try {
      setLoading(true);
      const task = await taskService.getTask(taskId);
      dispatch({ type: TASK_ACTIONS.SET_CURRENT_TASK, payload: task });
      return task;
    } catch (error) {
      setError(error.message);
      throw error;
    }
  };

  const createTask = async (taskData) => {
    try {
      setLoading(true);
      const newTask = await taskService.createTask(taskData);
      dispatch({ type: TASK_ACTIONS.ADD_TASK, payload: newTask });
      return newTask;
    } catch (error) {
      setError(error.message);
      throw error;
    }
  };

  const updateTask = async (taskId, taskData) => {
    try {
      setLoading(true);
      const updatedTask = await taskService.updateTask(taskId, taskData);
      dispatch({ type: TASK_ACTIONS.UPDATE_TASK, payload: updatedTask });
      return updatedTask;
    } catch (error) {
      setError(error.message);
      throw error;
    }
  };

  const deleteTask = async (taskId) => {
    try {
      setLoading(true);
      await taskService.deleteTask(taskId);
      dispatch({ type: TASK_ACTIONS.DELETE_TASK, payload: taskId });
    } catch (error) {
      setError(error.message);
      throw error;
    }
  };

  const updateTaskStatus = async (taskId, status, reason = '') => {
    try {
      setLoading(true);
      const updatedTask = await taskService.updateTaskStatus(taskId, status, reason);
      dispatch({ type: TASK_ACTIONS.UPDATE_TASK, payload: updatedTask });
      return updatedTask;
    } catch (error) {
      setError(error.message);
      throw error;
    }
  };

  const fetchStatistics = useCallback(async () => {
    const now = Date.now();
    if (now - lastFetchTime.current < FETCH_COOLDOWN) {
      console.log('Rate limiting: skipping fetch request');
      return state.statistics; // Return cached data
    }
    
    try {
      setLoading(true);
      lastFetchTime.current = now;
      const statistics = await taskService.getTaskStatistics();
      dispatch({ type: TASK_ACTIONS.SET_STATISTICS, payload: statistics });
      return statistics;
    } catch (error) {
      setError(error.message);
      throw error;
    } finally {
      setLoading(false);
    }
  }, [state.statistics]);

  const setFilters = (filters) => {
    dispatch({ type: TASK_ACTIONS.SET_FILTERS, payload: filters });
  };

  const setPagination = (pagination) => {
    dispatch({ type: TASK_ACTIONS.SET_PAGINATION, payload: pagination });
  };

  const resetFilters = () => {
    dispatch({ type: TASK_ACTIONS.RESET_FILTERS });
  };

  const clearCurrentTask = () => {
    dispatch({ type: TASK_ACTIONS.CLEAR_CURRENT_TASK });
  };

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
