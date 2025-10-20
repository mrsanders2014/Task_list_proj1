import '../styles/globals.css';
import { AuthProvider } from '../context/AuthContext';
import { TaskProvider } from '../context/TaskContext';
import ErrorBoundary from '../components/ErrorBoundary';
import { useEffect } from 'react';

function MyApp({ Component, pageProps }) {
  useEffect(() => {
    // Suppress browser extension errors globally
    const originalError = window.onerror;
    window.onerror = (message, source, lineno, colno, error) => {
      if (message && message.includes('listener indicated an asynchronous response')) {
        return true; // Suppress the error
      }
      if (originalError) {
        return originalError(message, source, lineno, colno, error);
      }
      return false;
    };

    // Also handle unhandled promise rejections
    const handleUnhandledRejection = (event) => {
      if (event.reason && event.reason.message && 
          event.reason.message.includes('listener indicated an asynchronous response')) {
        event.preventDefault();
      }
    };

    window.addEventListener('unhandledrejection', handleUnhandledRejection);

    return () => {
      window.onerror = originalError;
      window.removeEventListener('unhandledrejection', handleUnhandledRejection);
    };
  }, []);

  return (
    <ErrorBoundary>
      <AuthProvider>
        <TaskProvider>
          <Component {...pageProps} />
        </TaskProvider>
      </AuthProvider>
    </ErrorBoundary>
  );
}

export default MyApp;
