import React from 'react';

const ErrorMessage = ({
  message,
  title = 'Error',
  variant = 'error',
  onDismiss,
  className = '',
}) => {
  const variantStyles = {
    error: {
      backgroundColor: '#fef2f2',
      borderColor: '#fecaca',
      color: '#dc2626',
    },
    warning: {
      backgroundColor: '#fffbeb',
      borderColor: '#fed7aa',
      color: '#d97706',
    },
    info: {
      backgroundColor: '#eff6ff',
      borderColor: '#bfdbfe',
      color: '#2563eb',
    },
    success: {
      backgroundColor: '#f0fdf4',
      borderColor: '#bbf7d0',
      color: '#16a34a',
    },
  };
  
  const iconStyles = {
    error: { color: '#f87171' },
    warning: { color: '#fbbf24' },
    info: { color: '#60a5fa' },
    success: { color: '#4ade80' },
  };
  
  const iconPaths = {
    error: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z',
    warning: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z',
    info: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
    success: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
  };
  
  if (!message) return null;
  
  return (
    <div 
      className={`rounded-md border p-4 ${className}`}
      style={{
        ...variantStyles[variant],
        border: `1px solid ${variantStyles[variant].borderColor}`,
        borderRadius: '6px',
        padding: '16px',
      }}
    >
      <div className="flex">
        <div className="flex-shrink-0">
          <svg
            className="h-5 w-5"
            style={iconStyles[variant]}
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fillRule="evenodd"
              d={iconPaths[variant]}
              clipRule="evenodd"
            />
          </svg>
        </div>
        <div className="ml-3 flex-1">
          <h3 className="text-sm font-medium">{title}</h3>
          <div className="mt-1 text-sm">
            <p>{message}</p>
          </div>
        </div>
        {onDismiss && (
          <div className="ml-auto pl-3">
            <div className="-mx-1.5 -my-1.5">
              <button
                onClick={onDismiss}
                className="inline-flex rounded-md p-1.5 focus:outline-none focus:ring-2 focus:ring-offset-2"
                style={{
                  color: iconStyles[variant].color,
                  backgroundColor: 'transparent',
                  border: 'none',
                  cursor: 'pointer',
                }}
                onMouseEnter={(e) => {
                  e.target.style.backgroundColor = variantStyles[variant].backgroundColor;
                }}
                onMouseLeave={(e) => {
                  e.target.style.backgroundColor = 'transparent';
                }}
              >
                <span className="sr-only">Dismiss</span>
                <svg
                  className="h-5 w-5"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                    clipRule="evenodd"
                  />
                </svg>
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ErrorMessage;
