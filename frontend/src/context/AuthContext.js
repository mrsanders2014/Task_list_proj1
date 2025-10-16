import React, { createContext, useContext, useReducer, useEffect, useRef, useCallback } from 'react';
import authService from '../services/authService';

// Initial state
const initialState = {
  user: null,
  isAuthenticated: false,
  isLoading: true,
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
  const sessionTimeoutRef = useRef(null);
  const SESSION_TIMEOUT = 15 * 60 * 1000; // 15 minutes in milliseconds

  // Check authentication status on mount
  useEffect(() => {
    console.log('AuthContext: Component mounted, checking auth status');
    checkAuthStatus();
  }, []); // Empty dependency array to run only once

  // Session timeout management
  const resetSessionTimeout = useCallback(() => {
    if (sessionTimeoutRef.current) {
      clearTimeout(sessionTimeoutRef.current);
    }
    
    if (state.isAuthenticated) {
      // Reduced logging to prevent console spam
      sessionTimeoutRef.current = setTimeout(() => {
        console.log('AuthContext: Session timeout reached, logging out user');
        dispatch({ type: AUTH_ACTIONS.LOGOUT });
        if (typeof window !== 'undefined') {
          window.location.href = '/';
        }
      }, SESSION_TIMEOUT);
    }
  }, [state.isAuthenticated]);

  // Reset session timeout on user activity
  useEffect(() => {
    if (state.isAuthenticated) {
      const handleUserActivity = () => {
        // Reduced logging to prevent console spam
        resetSessionTimeout();
      };

      // Listen for user activity events
      const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];
      events.forEach(event => {
        document.addEventListener(event, handleUserActivity, true);
      });

      // Set initial timeout
      resetSessionTimeout();

      return () => {
        events.forEach(event => {
          document.removeEventListener(event, handleUserActivity, true);
        });
        if (sessionTimeoutRef.current) {
          clearTimeout(sessionTimeoutRef.current);
        }
      };
    }
  }, [state.isAuthenticated, resetSessionTimeout]);

  const checkAuthStatus = useCallback(async () => {
    try {
      dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: true });
      
      // Check if we have any cookies or localStorage token
      if (typeof document !== 'undefined') {
        const hasAuthCookie = document.cookie.includes('access_token=');
        const hasLocalStorageToken = localStorage.getItem('access_token');
        
        console.log('AuthContext: Checking authentication:', {
          hasAuthCookie,
          hasLocalStorageToken: !!hasLocalStorageToken,
          cookies: document.cookie,
          cookieLength: document.cookie.length,
          allCookies: document.cookie.split(';').map(c => c.trim())
        });
        
        if (!hasAuthCookie && !hasLocalStorageToken) {
          console.log('AuthContext: No auth cookie or localStorage token found, user not authenticated');
          dispatch({ type: AUTH_ACTIONS.LOGOUT });
          return;
        }
      }
      
      console.log('AuthContext: Getting current user...');
      const user = await authService.getCurrentUser();
      console.log('AuthContext: Current user retrieved:', user);
      dispatch({ type: AUTH_ACTIONS.SET_USER, payload: user });
    } catch (error) {
      console.log('Authentication check failed:', error.message);
      // Don't treat this as a login failure, just clear the user state
      dispatch({ type: AUTH_ACTIONS.LOGOUT });
    } finally {
      dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: false });
    }
  }, []); // Empty dependency array to prevent re-creation

  const login = async (credentials) => {
    try {
      dispatch({ type: AUTH_ACTIONS.LOGIN_START });
      const user = await authService.login(credentials);
      dispatch({ type: AUTH_ACTIONS.LOGIN_SUCCESS, payload: user });
      console.log('AuthContext: Login successful, session timeout will be set automatically');
      
      // Check if cookie was set after login
      if (typeof document !== 'undefined') {
        console.log('AuthContext: Cookies after login:', {
          cookies: document.cookie,
          cookieLength: document.cookie.length,
          allCookies: document.cookie.split(';').map(c => c.trim()),
          hasAccessToken: document.cookie.includes('access_token=')
        });
      }
      
      return user;
    } catch (error) {
      console.error('AuthContext: Login failed:', error);
      dispatch({ type: AUTH_ACTIONS.LOGIN_FAILURE, payload: error.message });
      throw error;
    }
  };

  const register = async (userData) => {
    try {
      dispatch({ type: AUTH_ACTIONS.LOGIN_START });
      const user = await authService.register(userData);
      dispatch({ type: AUTH_ACTIONS.LOGIN_SUCCESS, payload: user });
      return user;
    } catch (error) {
      dispatch({ type: AUTH_ACTIONS.LOGIN_FAILURE, payload: error.message });
      throw error;
    }
  };

  const logout = async () => {
    try {
      // Clear session timeout
      if (sessionTimeoutRef.current) {
        clearTimeout(sessionTimeoutRef.current);
        sessionTimeoutRef.current = null;
      }
      console.log('AuthContext: Logging out user, clearing session timeout');
      await authService.logout();
    } catch (error) {
      console.warn('Logout error:', error);
    } finally {
      // Clear localStorage token as well
      localStorage.removeItem('access_token');
      console.log('AuthContext: Token removed from localStorage');
      dispatch({ type: AUTH_ACTIONS.LOGOUT });
    }
  };

  const clearError = () => {
    dispatch({ type: AUTH_ACTIONS.CLEAR_ERROR });
  };

  const setError = (error) => {
    dispatch({ type: AUTH_ACTIONS.SET_ERROR, payload: error });
  };

  // Debug authentication state changes (reduced logging)
  useEffect(() => {
    if (process.env.NODE_ENV === 'development') {
      console.log('AuthContext: State changed:', {
        isAuthenticated: state.isAuthenticated,
        isLoading: state.isLoading,
        user: state.user ? { username: state.user.username, id: state.user.id } : null,
        error: state.error
      });
    }
  }, [state.isAuthenticated, state.isLoading, state.user, state.error]);

  const value = {
    ...state,
    login,
    register,
    logout,
    clearError,
    setError,
    checkAuthStatus,
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
