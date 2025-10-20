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
    redirectTo = '/', // Redirect to home page where login form is located
    requireAuth = true,
    loadingComponent: LoadingComponent = null,
  } = options;

  return function ProtectedComponent(props) {
    const { isAuthenticated, isLoading, user } = useAuth();
    const router = useRouter();

    useEffect(() => {
      // Add a small delay to ensure auth state is fully loaded
      const timer = setTimeout(() => {
        if (!isLoading) {
          if (requireAuth && !isAuthenticated) {
            // Redirecting to login - not authenticated
            router.push(redirectTo);
          } else if (!requireAuth && isAuthenticated) {
            // Redirecting to tasks - already authenticated
            router.push('/tasks');
          }
        }
      }, 100); // Small delay to ensure auth state is stable

      return () => clearTimeout(timer);
    }, [isAuthenticated, isLoading, router, user]);

    // Show loading component while checking authentication
    if (isLoading || (requireAuth && !user)) {
      return LoadingComponent || (
        <div className="min-h-screen flex items-center justify-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900"></div>
        </div>
      );
    }

    // Don't render the component if redirecting or not authenticated
    if (requireAuth && !isAuthenticated) {
      return (
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900 mx-auto"></div>
            <p className="mt-4 text-gray-600">Redirecting to login...</p>
          </div>
        </div>
      );
    }

    if (!requireAuth && isAuthenticated) {
      return (
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900 mx-auto"></div>
            <p className="mt-4 text-gray-600">Redirecting...</p>
          </div>
        </div>
      );
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
    redirectTo = '/', // Redirect to home page where login form is located
    requireAuth = true,
  } = options;

  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading) {
      if (requireAuth && !isAuthenticated) {
        router.push(redirectTo);
      } else if (!requireAuth && isAuthenticated) {
        router.push('/tasks');
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
  redirectTo = '/', // Redirect to home page where login form is located
  fallback = null 
}) => {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading) {
      if (requireAuth && !isAuthenticated) {
        router.push(redirectTo);
      } else if (!requireAuth && isAuthenticated) {
        router.push('/tasks');
      }
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return fallback;
  }

  if (requireAuth && !isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900 mx-auto"></div>
          <p className="mt-4 text-gray-600">Redirecting to login...</p>
        </div>
      </div>
    );
  }

  if (!requireAuth && isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900 mx-auto"></div>
          <p className="mt-4 text-gray-600">Redirecting...</p>
        </div>
      </div>
    );
  }

  return children;
};

export default {
  withAuth,
  useAuthGuard,
  AuthGuard,
};
