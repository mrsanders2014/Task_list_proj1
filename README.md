# Task Manager FastAPI Application

A MongoDB-based task management system with RESTful API built using FastAPI and Beanie ODM.

## Features

- **User Management**: Complete CRUD operations for users with Beanie ODM
- **Task Management**: Full CRUD operations with advanced filtering and relationships
- **Task Statistics**: Comprehensive statistics and analytics
- **Status Management**: Track task status changes with history
- **Priority & Label Support**: Organize tasks with priorities and labels
- **Due Date Management**: Set due dates and track overdue tasks
- **RESTful API**: Modern HTTP API with automatic documentation
- **Data Validation**: Comprehensive input validation and error handling
- **Async Operations**: Full async/await support with Beanie ODM

## Quick Start

### Installation

```bash
uv sync
```

### Configuration

Create a `.env` file with your MongoDB connection string:

```
project_db_url=mongodb://localhost:27017
DATABASE_NAME=task_manager
MOCK_MODE=false
```

**Note**: The application now uses Beanie ODM for MongoDB operations, providing better type safety and async support.

### Start the API Server

```bash
uv run python main.py
```

The API will be available at `http://localhost:8000`

### Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Users

- `POST /users/` - Create a new user
- `GET /users/` - Get all users (with optional filters)
- `GET /users/{user_id}` - Get user by ID
- `GET /users/username/{username}` - Get user by username
- `PUT /users/{user_id}` - Update user information
- `DELETE /users/{user_id}` - Delete a user
- `PATCH /users/{user_id}/status` - Change user active status

### Tasks

- `POST /tasks/` - Create a new task
- `GET /tasks/` - Get tasks (with optional filters)
- `GET /tasks/{task_id}` - Get task by ID
- `PUT /tasks/{task_id}` - Update task information
- `PATCH /tasks/{task_id}/status` - Update task status
- `DELETE /tasks/{task_id}` - Delete a task
- `GET /tasks/user/{user_id}` - Get all tasks for a specific user
- `GET /tasks/statistics/overview` - Get comprehensive task statistics


### Filtering Options

**Tasks:**
- Filter by user ID, status, priority range, labels, or overdue status
- Advanced query parameters for flexible data retrieval

## Example Usage

### Create a User

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Create a Task

```bash
curl -X POST "http://localhost:8000/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "USER_ID",
    "title": "Complete project documentation",
    "description": "Write comprehensive API documentation",
    "status": "Created",
    "priority": 3,
    "estimated_time": 4.0
  }'
```


## Project Structure

- `main.py` - Main FastAPI application entry point
- `src/api/` - FastAPI API endpoints
  - `beanie_users.py` - User API endpoints (Beanie ODM)
  - `beanie_tasks.py` - Task API endpoints (Beanie ODM)
  - `schemas.py` - Pydantic schemas for validation
- `src/models/` - Beanie ODM document models
  - `beanie_user.py` - User document model
  - `beanie_task.py` - Task document model
- `src/dbase/` - Database connection and initialization
  - `beanie_init.py` - Beanie ODM initialization
- `tests/` - Unit tests
  - `test_beanie_user.py` - User model tests
  - `test_beanie_task.py` - Task model tests

## Data Models

### BeanieUser Model

The BeanieUser model includes:

- Basic user information (username, email, first/last name)
- Account status and timestamps
- Full name generation and status management
- Unique constraints on username and email
- Automatic timestamp management

### BeanieTask Model

The BeanieTask model includes:

- Basic task information (title, description)
- User relationship via Beanie Link
- Status tracking (Created, Started, InProcess, Modified, Scheduled, Complete, Deleted)
- Optional labels for categorization
- Optional task management details:
  - Priority (1-10, where 1 is highest)
  - Due dates
  - Time estimates
  - Notifications
  - Time tracking history
- Complete task history with reasons for status changes


## Running Tests

```bash
uv run pytest tests/
```

## Development

### Code Formatting

```bash
uv run black src/
uv run ruff check src/
```

### Type Checking

```bash
uv run mypy src/
```

## Migration History

This application has undergone two major migrations:

### 1. CLI to FastAPI Migration
- ✅ Removed CLI interface (`src/User_int/`)
- ✅ Created FastAPI application with full CRUD endpoints
- ✅ Added comprehensive API documentation
- ✅ Implemented proper error handling and validation
- ✅ Added CORS support for web frontend integration

### 2. PyMongo to Beanie ODM Migration
- ✅ Migrated from PyMongo repositories to Beanie ODM
- ✅ Created new Beanie document models with proper relationships
- ✅ Implemented full async/await support
- ✅ Enhanced type safety and validation
- ✅ Added comprehensive test coverage for all models
- ✅ Improved database connection management

All functionality is now available through modern HTTP endpoints with proper REST conventions and async support.

## Architecture

- **FastAPI**: Modern, fast web framework for building APIs
- **Beanie ODM**: Async MongoDB object-document mapper
- **Pydantic**: Data validation and serialization
- **Motor**: Async MongoDB driver
- **MongoDB**: Document-based database
- **Uvicorn**: ASGI server for production deployment
- **CORS**: Cross-origin resource sharing for web integration

## Key Benefits of Beanie Migration

- **Type Safety**: Full type hints and validation throughout the application
- **Async Support**: Native async/await support for better performance
- **Relationships**: Proper document linking and relationship management
- **Validation**: Built-in Pydantic validation for all data models
- **Indexing**: Automatic index management for optimal query performance
- **Error Handling**: Comprehensive error handling with proper HTTP status codes
- **Extensibility**: Easy to add new fields and methods to models

