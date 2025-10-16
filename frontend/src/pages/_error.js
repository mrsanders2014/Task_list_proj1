import React from 'react';
import MainLayout from '../layouts/MainLayout';
import Button from '../components/Button';

const ErrorPage = ({ statusCode, hasGetInitialPropsRun, err }) => {
  const getErrorMessage = () => {
    if (statusCode === 404) {
      return {
        title: 'Page Not Found',
        message: 'The page you are looking for does not exist.',
        action: 'Go Home',
        actionHref: '/',
      };
    }
    
    if (statusCode === 500) {
      return {
        title: 'Server Error',
        message: 'Something went wrong on our end. Please try again later.',
        action: 'Go Home',
        actionHref: '/',
      };
    }
    
    return {
      title: 'An Error Occurred',
      message: 'Something went wrong. Please try again.',
      action: 'Go Home',
      actionHref: '/',
    };
  };

  const errorInfo = getErrorMessage();

  return (
    <MainLayout showFooter={false}>
      <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full text-center">
          <div className="mb-8">
            <h1 className="text-6xl font-bold text-gray-900 mb-4">
              {statusCode || 'Error'}
            </h1>
            <h2 className="text-2xl font-semibold text-gray-700 mb-4">
              {errorInfo.title}
            </h2>
            <p className="text-gray-600 mb-8">
              {errorInfo.message}
            </p>
          </div>
          
          <div className="space-y-4">
            <Button
              onClick={() => window.location.href = errorInfo.actionHref}
              className="w-full"
            >
              {errorInfo.action}
            </Button>
            
            <Button
              variant="outline"
              onClick={() => window.history.back()}
              className="w-full"
            >
              Go Back
            </Button>
          </div>
          
          {process.env.NODE_ENV === 'development' && err && (
            <div className="mt-8 p-4 bg-red-50 border border-red-200 rounded-md text-left">
              <h3 className="text-sm font-medium text-red-800 mb-2">
                Development Error Details:
              </h3>
              <pre className="text-xs text-red-700 whitespace-pre-wrap">
                {err.message}
                {err.stack}
              </pre>
            </div>
          )}
        </div>
      </div>
    </MainLayout>
  );
};

ErrorPage.getInitialProps = ({ res, err }) => {
  const statusCode = res ? res.statusCode : err ? err.statusCode : 404;
  return { statusCode };
};

export default ErrorPage;
