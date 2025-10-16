import React from 'react';
import MainLayout from '../layouts/MainLayout';
import Button from '../components/Button';

const Custom404 = () => {
  return (
    <MainLayout showFooter={false}>
      <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full text-center">
          <div className="mb-8">
            <h1 className="text-6xl font-bold text-gray-900 mb-4">404</h1>
            <h2 className="text-2xl font-semibold text-gray-700 mb-4">
              Page Not Found
            </h2>
            <p className="text-gray-600 mb-8">
              The page you are looking for does not exist or has been moved.
            </p>
          </div>
          
          <div className="space-y-4">
            <Button
              onClick={() => window.location.href = '/'}
              className="w-full"
            >
              Go Home
            </Button>
            
            <Button
              variant="outline"
              onClick={() => window.history.back()}
              className="w-full"
            >
              Go Back
            </Button>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default Custom404;
