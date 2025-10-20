import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { useTask } from '../../../context/TaskContext';
import { withAuth } from '../../../middleware/authMiddleware';
import MainLayout from '../../../layouts/MainLayout';
import Card from '../../../components/Card';
import TaskForm from '../../../components/TaskForm';
import Button from '../../../components/Button';
import Loader from '../../../components/Loader';
import ErrorMessage from '../../../components/ErrorMessage';

const EditTaskPage = () => {
  const { currentTask, fetchTask, updateTask, error, clearError } = useTask();
  const router = useRouter();
  const { id } = router.query;
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (id) {
      fetchTask(id);
    }
  }, [id, fetchTask]);

  const handleUpdate = async (taskData) => {
    try {
      setIsSubmitting(true);
      await updateTask(id, taskData);
      router.push('/tasks');
    } catch (error) {
      console.error('Error updating task:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCancel = () => {
    router.push('/tasks');
  };

  if (!currentTask && !error) {
    return (
      <MainLayout showFooter={false}>
        <div className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
          <Loader size="lg" text="Loading task..." />
        </div>
      </MainLayout>
    );
  }

  if (!currentTask) {
    return (
      <MainLayout showFooter={false}>
        <div className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="text-center py-12">
            <h3 className="text-lg font-medium text-gray-900">Task not found</h3>
            <p className="mt-1 text-sm text-gray-500">
              The task you&apos;re looking for doesn&apos;t exist or has been deleted.
            </p>
            <div className="mt-6">
              <Button onClick={() => router.push('/tasks')}>
                Back to Tasks
              </Button>
            </div>
          </div>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout showFooter={false}>
      <div className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Edit Task</h1>
          <p className="mt-2 text-gray-600">
            Modify the task details below. The title cannot be changed.
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
            task={currentTask}
            onSubmit={handleUpdate}
            onCancel={handleCancel}
            isLoading={isSubmitting}
            isEditMode={true}
          />
        </Card>
      </div>
    </MainLayout>
  );
};

export default withAuth(EditTaskPage);
