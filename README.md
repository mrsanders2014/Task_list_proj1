# Task Manager FastAPI Application

A MongoDB-based task management system with RESTful API built using FastAPI.

## Features

- **User Management**: Complete CRUD operations for users
- **Task Management**: Full CRUD operations with advanced filtering
- **Task Statistics**: Comprehensive statistics and analytics
- **Status Management**: Track task status changes with history
- **Priority & Label Support**: Organize tasks with priorities and labels
- **Due Date Management**: Set due dates and track overdue tasks
- **RESTful API**: Modern HTTP API with automatic documentation
- **Data Validation**: Comprehensive input validation and error handling

## Quick Start

### Installation

```bash
uv sync
```

### Configuration

Create a `.env` file with your MongoDB connection string:

```
MONGO_URI=mongodb://localhost:27017
DB_NAME=task_manager
```

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
- `DELETE /tasks/{task_id}` - Delete a task (soft or hard)
- `GET /tasks/user/{user_id}/statistics` - Get task statistics for user

### Task Filtering Options

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
curl -X POST "http://localhost:8000/tasks/?user_id=USER_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive API documentation",
    "status": "Created",
    "task_mgmt": {
      "priority": 3,
      "time_unit": "hours",
      "estimated_time_to_complete": 4.0
    }
  }'
```

## Project Structure

- `src/api/` - FastAPI application and endpoints
  - `main.py` - Main FastAPI application
  - `schemas.py` - Pydantic schemas for validation
  - `users.py` - User API endpoints
  - `tasks.py` - Task API endpoints
- `src/model/` - Data models (User, Task)
- `src/dbase/` - Database repositories and connection
- `tests/` - Unit tests

## Data Models

### Task Model

The Task model includes:

- Basic task information (title, description)
- Status tracking (Created, Started, InProcess, Modified, Scheduled, Complete, Deleted)
- Optional labels for categorization
- Optional task management details:
  - Priority (1-10, where 1 is highest)
  - Due dates
  - Time estimates
  - Notifications
  - Time tracking history
- Complete task history with reasons for status changes

### User Model

The User model includes:

- Basic user information (username, email, first/last name)
- Account status and timestamps
- Full name generation and status management

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

## Migration from CLI

This application has been completely refactored from a CLI-based system to a RESTful API:

- ✅ Removed CLI interface (`src/User_int/`)
- ✅ Created FastAPI application with full CRUD endpoints
- ✅ Maintained all existing data models and repositories
- ✅ Added comprehensive API documentation
- ✅ Implemented proper error handling and validation
- ✅ Added CORS support for web frontend integration

All existing functionality is now available through HTTP endpoints with proper REST conventions.

## Architecture

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and serialization
- **MongoDB**: Document-based database with PyMongo
- **Uvicorn**: ASGI server for production deployment
- **CORS**: Cross-origin resource sharing for web integration

