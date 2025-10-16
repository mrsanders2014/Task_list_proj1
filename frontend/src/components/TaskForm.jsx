import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import Input from './Input';
import Button from './Button';
import { TASK_STATUS_OPTIONS, PRIORITY_OPTIONS, TIME_UNITS } from '../constants';

const TaskForm = ({
  task = null,
  onSubmit,
  onCancel,
  isLoading = false,
  className = '',
}) => {
  const [labels, setLabels] = useState([]);
  const [newLabel, setNewLabel] = useState({ name: '', color: '#808080' });
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    watch,
    reset,
  } = useForm({
    defaultValues: {
      title: '',
      description: '',
      status: 'Created',
      priority: 1,
      due_date: '',
      estimated_time: '',
      time_unit: 'hours',
    },
  });

  useEffect(() => {
    if (task) {
      reset({
        title: task.title || '',
        description: task.description || '',
        status: task.status || 'Created',
        priority: task.task_mgmt?.priority || 1,
        due_date: task.task_mgmt?.duedate ? new Date(task.task_mgmt.duedate).toISOString().split('T')[0] : '',
        estimated_time: task.task_mgmt?.estimated_time_to_complete || '',
        time_unit: task.task_mgmt?.time_unit || 'hours',
      });
      setLabels(task.labels || []);
    }
  }, [task, reset]);

  const addLabel = () => {
    if (newLabel.name.trim()) {
      setLabels([...labels, { ...newLabel, name: newLabel.name.trim() }]);
      setNewLabel({ name: '', color: '#808080' });
    }
  };

  const removeLabel = (index) => {
    setLabels(labels.filter((_, i) => i !== index));
  };

  const handleFormSubmit = (data) => {
    const formData = {
      ...data,
      labels: labels,
      task_mgmt: {
        priority: parseInt(data.priority),
        duedate: data.due_date ? new Date(data.due_date).toISOString() : null,
        estimated_time_to_complete: data.estimated_time ? parseFloat(data.estimated_time) : null,
        time_unit: data.time_unit,
      },
    };
    
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className={`space-y-6 ${className}`}>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="md:col-span-2">
          <Input
            label="Title"
            {...register('title', { required: 'Title is required' })}
            error={errors.title?.message}
            placeholder="Enter task title"
          />
        </div>
        
        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            {...register('description')}
            rows={3}
            className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500"
            placeholder="Enter task description"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Status
          </label>
          <select
            {...register('status')}
            className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500"
          >
            {TASK_STATUS_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Priority
          </label>
          <select
            {...register('priority', { valueAsNumber: true })}
            className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500"
          >
            {PRIORITY_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        
        <div>
          <Input
            label="Due Date"
            type="date"
            {...register('due_date')}
            error={errors.due_date?.message}
          />
        </div>
        
        <div>
          <div className="flex space-x-2">
            <div className="flex-1">
              <Input
                label="Estimated Time"
                type="number"
                step="0.5"
                min="0"
                {...register('estimated_time', { valueAsNumber: true })}
                error={errors.estimated_time?.message}
                placeholder="0"
              />
            </div>
            <div className="w-24">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Unit
              </label>
              <select
                {...register('time_unit')}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500"
              >
                {TIME_UNITS.map((unit) => (
                  <option key={unit.value} value={unit.value}>
                    {unit.label}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </div>
      
      {/* Labels Section */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Labels
        </label>
        <div className="space-y-3">
          <div className="flex space-x-2">
            <Input
              placeholder="Label name"
              value={newLabel.name}
              onChange={(e) => setNewLabel({ ...newLabel, name: e.target.value })}
              className="flex-1"
            />
            <input
              type="color"
              value={newLabel.color}
              onChange={(e) => setNewLabel({ ...newLabel, color: e.target.value })}
              className="w-12 h-10 border border-gray-300 rounded-md cursor-pointer"
            />
            <Button type="button" onClick={addLabel} variant="outline">
              Add
            </Button>
          </div>
          
          {labels.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {labels.map((label, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
                  style={{ backgroundColor: label.color + '20', color: label.color }}
                >
                  {label.name}
                  <button
                    type="button"
                    onClick={() => removeLabel(index)}
                    className="ml-2 text-gray-500 hover:text-gray-700"
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
      
      {/* Form Actions */}
      <div className="flex justify-end space-x-3 pt-6 border-t border-gray-200">
        <Button
          type="button"
          variant="outline"
          onClick={onCancel}
          disabled={isLoading}
        >
          Cancel
        </Button>
        <Button
          type="submit"
          loading={isLoading}
        >
          {task ? 'Update Task' : 'Create Task'}
        </Button>
      </div>
    </form>
  );
};

export default TaskForm;
