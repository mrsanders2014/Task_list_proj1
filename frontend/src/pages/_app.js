import '../styles/globals.css';
import { AuthProvider } from '../context/AuthContext';
import { TaskProvider } from '../context/TaskContext';

function MyApp({ Component, pageProps }) {
  return (
    <AuthProvider>
      <TaskProvider>
        <Component {...pageProps} />
      </TaskProvider>
    </AuthProvider>
  );
}

export default MyApp;
