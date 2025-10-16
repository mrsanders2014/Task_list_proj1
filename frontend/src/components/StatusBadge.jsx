import React from 'react';
import { TASK_STATUS_OPTIONS } from '../constants';

const StatusBadge = ({ status, size = 'sm', className = '' }) => {
  const statusOption = TASK_STATUS_OPTIONS.find(option => option.value === status);
  
  if (!statusOption) {
    return (
      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800 ${className}`}>
        Unknown
      </span>
    );
  }
  
  const sizeClasses = {
    xs: 'px-1.5 py-0.5 text-xs',
    sm: 'px-2 py-1 text-xs',
    md: 'px-2.5 py-1.5 text-sm',
    lg: 'px-3 py-2 text-base',
  };
  
  return (
    <span className={`inline-flex items-center rounded-full font-medium text-white ${sizeClasses[size]} ${statusOption.color} ${className}`}>
      {statusOption.label}
    </span>
  );
};

export default StatusBadge;
