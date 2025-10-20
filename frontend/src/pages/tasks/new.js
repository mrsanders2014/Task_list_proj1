import React, { useState } from 'react';
import { useRouter } from 'next/router';
import { useTask } from '../../context/TaskContext';
import { withAuth } from '../../middleware/authMiddleware';
import MainLayout from '../../layouts/MainLayout';
import Card from '../../components/Card';
import TaskForm from '../../components/TaskForm';
import ErrorMessage from '../../components/ErrorMessage';

const NewTaskPage = () => {
  const { createTask, error, clearError } = useTask();
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (taskData) => {
    // Prevent multiple submissions
    if (isSubmitting) {
      return;
    }

    try {
      setIsSubmitting(true);
      await createTask(taskData);
      router.push('/tasks');
    } catch (error) {
      // Error will be handled by the TaskContext and displayed via the error state
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCancel = () => {
    router.push('/tasks');
  };

  return (
    <MainLayout showFooter={false}>
      <div className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Create New Task</h1>
          <p className="mt-2 text-gray-600">
            Add a new task to your task list
          </p>
        </div>

        {error && (
          <div className="mb-6">
            <ErrorMessage
              message={error}
              onDismiss={clearError}
            />
          </div>
        )}

        {/* Task Form */}
        <Card>
          <TaskForm
            onSubmit={handleSubmit}
            onCancel={handleCancel}
            isLoading={isSubmitting}
          />
        </Card>
      </div>
    </MainLayout>
  );
};

export default withAuth(NewTaskPage);
