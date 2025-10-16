import React, { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import Input from './Input';
import Button from './Button';

const UserForm = ({
  user = null,
  onSubmit,
  onCancel,
  isLoading = false,
  isEdit = false,
  className = '',
}) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm({
    defaultValues: {
      username: '',
      email: '',
      first_name: '',
      last_name: '',
      password: '',
      confirmPassword: '',
    },
  });

  useEffect(() => {
    if (user) {
      reset({
        username: user.username || '',
        email: user.email || '',
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        password: '',
        confirmPassword: '',
      });
    }
  }, [user, reset]);

  const handleFormSubmit = (data) => {
    // Remove confirmPassword from the data
    const { confirmPassword, ...formData } = data;
    
    // Only include password if it's provided (for updates)
    if (isEdit && !formData.password) {
      delete formData.password;
    }
    
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className={`space-y-6 ${className}`}>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <Input
            label="Username"
            {...register('username', {
              required: 'Username is required',
              minLength: {
                value: 3,
                message: 'Username must be at least 3 characters',
              },
              maxLength: {
                value: 50,
                message: 'Username must be less than 50 characters',
              },
            })}
            error={errors.username?.message}
            placeholder="Enter username"
            disabled={isEdit} // Username cannot be changed after creation
          />
        </div>
        
        <div>
          <Input
            label="Email"
            type="email"
            {...register('email', {
              required: 'Email is required',
              pattern: {
                value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                message: 'Please enter a valid email address',
              },
            })}
            error={errors.email?.message}
            placeholder="Enter email address"
          />
        </div>
        
        <div>
          <Input
            label="First Name"
            {...register('first_name', {
              maxLength: {
                value: 50,
                message: 'First name must be less than 50 characters',
              },
            })}
            error={errors.first_name?.message}
            placeholder="Enter first name"
          />
        </div>
        
        <div>
          <Input
            label="Last Name"
            {...register('last_name', {
              maxLength: {
                value: 50,
                message: 'Last name must be less than 50 characters',
              },
            })}
            error={errors.last_name?.message}
            placeholder="Enter last name"
          />
        </div>
        
        <div>
          <Input
            label={isEdit ? 'New Password (optional)' : 'Password'}
            type="password"
            {...register('password', {
              required: !isEdit ? 'Password is required' : false,
              minLength: {
                value: 6,
                message: 'Password must be at least 6 characters',
              },
            })}
            error={errors.password?.message}
            placeholder={isEdit ? 'Leave blank to keep current password' : 'Enter password'}
          />
        </div>
        
        {!isEdit && (
          <div>
            <Input
              label="Confirm Password"
              type="password"
              {...register('confirmPassword', {
                required: !isEdit ? 'Please confirm your password' : false,
                validate: (value) => {
                  if (!isEdit) {
                    const password = document.querySelector('input[name="password"]').value;
                    return value === password || 'Passwords do not match';
                  }
                  return true;
                },
              })}
              error={errors.confirmPassword?.message}
              placeholder="Confirm password"
            />
          </div>
        )}
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
          {isEdit ? 'Update User' : 'Create User'}
        </Button>
      </div>
    </form>
  );
};

export default UserForm;
