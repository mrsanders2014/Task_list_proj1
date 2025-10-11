# Task Manager FastAPI Application

This application has been refactored from a CLI-based system to a RESTful API using FastAPI and migrated to use Beanie ODM for MongoDB operations.

## Features

- **User Management**: Create, read, update, and delete users with Beanie ODM
- **Task Management**: Full CRUD operations for tasks with advanced filtering and relationships
- **Task Statistics**: Get comprehensive statistics for user tasks
- **Status Management**: Update task status with history tracking
- **Priority & Label Support**: Organize tasks with priorities and labels
- **Due Date Management**: Set due dates and track overdue tasks
- **Async Operations**: Full async/await support with Beanie ODM

## Quick Start

### 1. Install Dependencies

```bash
uv sync
```

### 2. Start the Application

```bash
uv run python main.py
```

The API will be available at `http://localhost:8000`

### 3. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/` | Create a new user |
| GET | `/users/` | Get all users (with optional filters) |
| GET | `/users/{user_id}` | Get user by ID |
| GET | `/users/username/{username}` | Get user by username |
| PUT | `/users/{user_id}` | Update user information |
| DELETE | `/users/{user_id}` | Delete a user |
| PATCH | `/users/{user_id}/status` | Change user active status |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks/` | Create a new task |
| GET | `/tasks/` | Get tasks (with optional filters) |
| GET | `/tasks/{task_id}` | Get task by ID |
| PUT | `/tasks/{task_id}` | Update task information |
| PATCH | `/tasks/{task_id}/status` | Update task status |
| DELETE | `/tasks/{task_id}` | Delete a task |
| GET | `/tasks/user/{user_id}` | Get all tasks for a specific user |
| GET | `/tasks/statistics/overview` | Get comprehensive task statistics |


### Query Parameters

**GET /tasks/:**
- `user_id`: Filter by user ID
- `task_status`: Filter by task status
- `min_priority`: Minimum priority level (1-10)
- `max_priority`: Maximum priority level (1-10)
- `label_name`: Filter by label name
- `overdue_only`: Show only overdue tasks (true/false)
- `skip`: Number of tasks to skip (pagination)
- `limit`: Maximum number of tasks to return (pagination)


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
    "estimated_time": 4.0,
    "labels": [
      {
        "name": "documentation",
        "color": "#3498db"
      }
    ]
  }'
```


### Get User Tasks

```bash
curl "http://localhost:8000/tasks/?user_id=USER_ID"
```

### Update Task Status

```bash
curl -X PATCH "http://localhost:8000/tasks/TASK_ID/status" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "InProcess",
    "reason": "Started working on the task"
  }'
```

### Get Task Statistics

```bash
curl "http://localhost:8000/tasks/statistics/overview"
```


## Data Models

### User Schema

```json
{
  "username": "string",
  "email": "string",
  "first_name": "string (optional)",
  "last_name": "string (optional)"
}
```

### Task Schema

```json
{
  "user_id": "string (required)",
  "title": "string (max 50 chars)",
  "description": "string (max 250 chars, optional)",
  "status": "Created|Started|InProcess|Modified|Scheduled|Complete|Deleted",
  "priority": "number (1-10, optional)",
  "estimated_time": "number (optional)",
  "due_date": "datetime (optional)",
  "labels": [
    {
      "name": "string",
      "color": "#hexcolor"
    }
  ]
}
```


## Configuration

The application uses environment variables for configuration:

- `project_db_url`: MongoDB connection string
- `DATABASE_NAME`: Database name
- `MOCK_MODE`: Set to 'true' for testing without MongoDB connection

Create a `.env` file in the project root:

```
project_db_url=mongodb://localhost:27017
DATABASE_NAME=task_manager
MOCK_MODE=false
```

**Note**: The application now uses Beanie ODM for MongoDB operations, providing better type safety and async support.

## Development

### Running Tests

```bash
uv run pytest
```

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

The application has undergone two major migrations:

### 1. CLI to FastAPI Migration
- ✅ Removed CLI interface (`src/User_int/cli.py`)
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
