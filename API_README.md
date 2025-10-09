# Task Manager FastAPI Application

This application has been refactored from a CLI-based system to a RESTful API using FastAPI.

## Features

- **User Management**: Create, read, update, and delete users
- **Task Management**: Full CRUD operations for tasks with advanced filtering
- **Task Statistics**: Get comprehensive statistics for user tasks
- **Status Management**: Update task status with history tracking
- **Priority & Label Support**: Organize tasks with priorities and labels
- **Due Date Management**: Set due dates and track overdue tasks

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
| DELETE | `/tasks/{task_id}` | Delete a task (soft or hard) |
| GET | `/tasks/user/{user_id}/statistics` | Get task statistics for user |

### Query Parameters for GET /tasks/

- `user_id`: Filter by user ID
- `status`: Filter by task status
- `min_priority`: Minimum priority level (1-10)
- `max_priority`: Maximum priority level (1-10)
- `label_name`: Filter by label name
- `overdue_only`: Show only overdue tasks (true/false)

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
    },
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
curl "http://localhost:8000/tasks/user/USER_ID/statistics"
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
  "title": "string (max 50 chars)",
  "description": "string (max 250 chars, optional)",
  "status": "Created|Started|InProcess|Modified|Scheduled|Complete|Deleted",
  "labels": [
    {
      "name": "string",
      "color": "#hexcolor"
    }
  ],
  "task_mgmt": {
    "priority": 1-10,
    "duedate": "datetime (optional)",
    "time_unit": "minutes|hours|days|weeks|months|years",
    "estimated_time_to_complete": "number (optional)",
    "notify_time": "number",
    "notify_time_units": "minutes|hours|days|weeks|months|years",
    "notification_wanted": "Y|N"
  }
}
```

## Configuration

The application uses environment variables for configuration:

- `MONGO_URI`: MongoDB connection string
- `DB_NAME`: Database name

Create a `.env` file in the project root:

```
MONGO_URI=mongodb://localhost:27017
DB_NAME=task_manager
```

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

## Migration from CLI

The application has been completely refactored from CLI to API:

- ✅ Removed CLI interface (`src/User_int/cli.py`)
- ✅ Created FastAPI application with full CRUD endpoints
- ✅ Maintained all existing data models and repositories
- ✅ Added comprehensive API documentation
- ✅ Implemented proper error handling and validation
- ✅ Added CORS support for web frontend integration

All existing functionality is now available through HTTP endpoints with proper REST conventions.
