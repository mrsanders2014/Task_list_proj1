import React, { createContext, useContext, useReducer, useEffect, useCallback } from 'react';
import authService from '../services/authService';

// Initial state
const initialState = {
  user: null,
  isAuthenticated: false,
  isLoading: false, // Start with false to prevent hanging on loading
  error: null,
};

// Action types
const AUTH_ACTIONS = {
  LOGIN_START: 'LOGIN_START',
  LOGIN_SUCCESS: 'LOGIN_SUCCESS',
  LOGIN_FAILURE: 'LOGIN_FAILURE',
  LOGOUT: 'LOGOUT',
  SET_LOADING: 'SET_LOADING',
  SET_ERROR: 'SET_ERROR',
  CLEAR_ERROR: 'CLEAR_ERROR',
  SET_USER: 'SET_USER',
};

// Reducer
const authReducer = (state, action) => {
  switch (action.type) {
    case AUTH_ACTIONS.LOGIN_START:
      return {
        ...state,
        isLoading: true,
        error: null,
      };
    case AUTH_ACTIONS.LOGIN_SUCCESS:
      return {
        ...state,
        user: action.payload,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      };
    case AUTH_ACTIONS.LOGIN_FAILURE:
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: action.payload,
      };
    case AUTH_ACTIONS.LOGOUT:
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      };
    case AUTH_ACTIONS.SET_LOADING:
      return {
        ...state,
        isLoading: action.payload,
      };
    case AUTH_ACTIONS.SET_ERROR:
      return {
        ...state,
        error: action.payload,
        isLoading: false,
      };
    case AUTH_ACTIONS.CLEAR_ERROR:
      return {
        ...state,
        error: null,
      };
    case AUTH_ACTIONS.SET_USER:
      return {
        ...state,
        user: action.payload,
        isAuthenticated: !!action.payload,
        isLoading: false,
        error: null,
      };
    default:
      return state;
  }
};

// Create context
const AuthContext = createContext();

// Auth provider component
export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);
  
  // Check authentication status on mount
  useEffect(() => {
    let isMounted = true;
    
    const checkAuthStatus = async () => {
      try {
        if (isMounted) {
          dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: true });
        }
        
        const user = await authService.getCurrentUser();
        
        if (isMounted) {
          dispatch({ type: AUTH_ACTIONS.SET_USER, payload: user });
        }
      } catch (error) {
        if (!isMounted) return;
        
        // Handle different types of errors silently
        if (error.code === 'ECONNABORTED' || error.message.includes('timeout') || error.code === 'TIMEOUT') {
          // Don't show timeout errors to user, just silently fail authentication check
        } else if (error.response?.status === 401) {
          // User not authenticated - this is normal
        } else if (error.response?.status >= 500) {
          // Server error during authentication check
        } else if (!error.response) {
          // Network error during authentication check
        } else {
          // Authentication check failed
        }
        
        // Always set loading to false and user to null on error
        dispatch({ type: AUTH_ACTIONS.SET_USER, payload: null });
        dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: false });
      }
    };

    checkAuthStatus();
    
    return () => {
      isMounted = false;
    };
  }, []);

  const login = useCallback(async (credentials) => {
    try {
      dispatch({ type: AUTH_ACTIONS.LOGIN_START });
      const user = await authService.login(credentials);
      dispatch({ type: AUTH_ACTIONS.LOGIN_SUCCESS, payload: user });
      return user;
    } catch (error) {
      // Ensure we always have a user-friendly error message
      const errorMessage = error.message || 'Login failed. Please try again.';
      dispatch({ type: AUTH_ACTIONS.LOGIN_FAILURE, payload: errorMessage });
      
      // Re-throw the error with the user-friendly message
      throw new Error(errorMessage);
    }
  }, []);

  const register = useCallback(async (userData) => {
    try {
      dispatch({ type: AUTH_ACTIONS.LOGIN_START });
      const user = await authService.register(userData);
      dispatch({ type: AUTH_ACTIONS.LOGIN_SUCCESS, payload: user });
      return user;
    } catch (error) {
      dispatch({ type: AUTH_ACTIONS.LOGIN_FAILURE, payload: error.message });
      throw error;
    }
  }, []);

  const logout = useCallback(async () => {
    try {
      await authService.logout();
    } catch (error) {
      console.warn('Logout error:', error);
    } finally {
      dispatch({ type: AUTH_ACTIONS.LOGOUT });
    }
  }, []);

  const clearError = useCallback(() => {
    dispatch({ type: AUTH_ACTIONS.CLEAR_ERROR });
  }, []);

  const setError = useCallback((error) => {
    dispatch({ type: AUTH_ACTIONS.SET_ERROR, payload: error });
  }, []);

  const value = {
    ...state,
    login,
    register,
    logout,
    clearError,
    setError,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;