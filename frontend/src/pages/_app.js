import '../styles/globals.css';
import { AuthProvider } from '../context/AuthContext';
import { TaskProvider } from '../context/TaskContext';
import ErrorBoundary from '../components/ErrorBoundary';

function MyApp({ Component, pageProps }) {
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
