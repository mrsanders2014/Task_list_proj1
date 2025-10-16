import { useAuth } from '../context/AuthContext';
import { useRouter } from 'next/router';
import { useEffect } from 'react';

/**
 * Higher-order component for protecting routes that require authentication
 * @param {React.Component} WrappedComponent - Component to protect
 * @param {Object} options - Protection options
 * @returns {React.Component} Protected component
 */
export const withAuth = (WrappedComponent, options = {}) => {
  const {
    redirectTo = '/login',
    requireAuth = true,
    loadingComponent: LoadingComponent = null,
  } = options;

  return function ProtectedComponent(props) {
    const { isAuthenticated, isLoading } = useAuth();
    const router = useRouter();

    useEffect(() => {
      if (!isLoading) {
        if (requireAuth && !isAuthenticated) {
          // Redirect to login if authentication is required but user is not authenticated
          router.push(redirectTo);
        } else if (!requireAuth && isAuthenticated) {
          // Redirect away from auth pages if user is already authenticated
          router.push('/dashboard');
        }
      }
    }, [isAuthenticated, isLoading, router]);

    // Show loading component while checking authentication
    if (isLoading) {
      return LoadingComponent || (
        <div className="min-h-screen flex items-center justify-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900"></div>
        </div>
      );
    }

    // Don't render the component if redirecting
    if (requireAuth && !isAuthenticated) {
      return null;
    }

    if (!requireAuth && isAuthenticated) {
      return null;
    }

    return <WrappedComponent {...props} />;
  };
};

/**
 * Hook for checking authentication status and redirecting if needed
 * @param {Object} options - Options for authentication check
 * @returns {Object} Authentication status and utilities
 */
export const useAuthGuard = (options = {}) => {
  const {
    redirectTo = '/login',
    requireAuth = true,
  } = options;

  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading) {
      if (requireAuth && !isAuthenticated) {
        router.push(redirectTo);
      } else if (!requireAuth && isAuthenticated) {
        router.push('/dashboard');
      }
    }
  }, [isAuthenticated, isLoading, router]);

  return {
    isAuthenticated,
    isLoading,
    shouldRender: requireAuth ? isAuthenticated : !isAuthenticated,
  };
};

/**
 * Component for conditional rendering based on authentication status
 * @param {Object} props - Component props
 * @returns {React.Component|null} Rendered component or null
 */
export const AuthGuard = ({ 
  children, 
  requireAuth = true, 
  redirectTo = '/login',
  fallback = null 
}) => {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading) {
      if (requireAuth && !isAuthenticated) {
        router.push(redirectTo);
      } else if (!requireAuth && isAuthenticated) {
        router.push('/dashboard');
      }
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return fallback;
  }

  if (requireAuth && !isAuthenticated) {
    return null;
  }

  if (!requireAuth && isAuthenticated) {
    return null;
  }

  return children;
};

export default {
  withAuth,
  useAuthGuard,
  AuthGuard,
};
