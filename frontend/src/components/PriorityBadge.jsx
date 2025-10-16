import React from 'react';
import { PRIORITY_OPTIONS } from '../constants';

const PriorityBadge = ({ priority, size = 'sm', className = '' }) => {
  const priorityOption = PRIORITY_OPTIONS.find(option => option.value === priority);
  
  if (!priorityOption) {
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
    <span className={`inline-flex items-center rounded-full font-medium ${sizeClasses[size]} ${priorityOption.color} ${className}`}>
      {priorityOption.label}
    </span>
  );
};

export default PriorityBadge;
