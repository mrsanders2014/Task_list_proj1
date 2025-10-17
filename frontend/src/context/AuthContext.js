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
  console.log('AuthProvider: Component rendering');
  const [state, dispatch] = useReducer(authReducer, initialState);
  console.log('AuthProvider: Initial state:', state);
  
  // Check authentication status on mount
  useEffect(() => {
    console.log('AuthContext: useEffect triggered - starting authentication check');
    let isMounted = true;
    
    const checkAuthStatus = async () => {
      try {
        console.log('AuthContext: Starting authentication check...');
        if (isMounted) {
          dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: true });
        }
        
        const user = await authService.getCurrentUser();
        
        if (isMounted) {
          console.log('AuthContext: Authentication successful:', user);
          dispatch({ type: AUTH_ACTIONS.SET_USER, payload: user });
        }
      } catch (error) {
        if (!isMounted) return;
        
        // Handle 401 errors gracefully (user not authenticated)
        if (error.response?.status === 401) {
          console.log('AuthContext: User not authenticated (401) - this is normal');
        } else {
          console.log('AuthContext: Authentication check failed:', error.message);
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
      console.log('AuthContext: Starting login process');
      dispatch({ type: AUTH_ACTIONS.LOGIN_START });
      console.log('AuthContext: Calling authService.login');
      const user = await authService.login(credentials);
      console.log('AuthContext: Login successful, user:', user);
      dispatch({ type: AUTH_ACTIONS.LOGIN_SUCCESS, payload: user });
      return user;
    } catch (error) {
      console.error('AuthContext: Login failed - caught error');
      console.error('AuthContext: Error type:', error.constructor.name);
      console.error('AuthContext: Error message:', error.message);
      
      // Ensure we always have a user-friendly error message
      const errorMessage = error.message || 'Login failed. Please try again.';
      console.log('AuthContext: Dispatching LOGIN_FAILURE with message:', errorMessage);
      dispatch({ type: AUTH_ACTIONS.LOGIN_FAILURE, payload: errorMessage });
      
      // Re-throw the error with the user-friendly message
      console.log('AuthContext: Re-throwing error with message:', errorMessage);
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