# Task List Project

A MongoDB-based task management system with Python CLI interface.

## Features

- User authentication and management
- Task CRUD operations with comprehensive metadata
- Task management details (priority, due dates, time estimates)
- Task history tracking
- Label categorization
- Time management tracking
- Rich CLI interface

## Installation

```bash
uv sync
```

## Configuration

Create a `.env` file with your MongoDB connection string:

```
project_db_url=mongodb://localhost:27017/
DATABASE_NAME=task_manager
```

## Usage

Run the CLI:

```bash
uv run python -m main
```

## Running Tests

```bash
uv run pytest tests/
```

## Project Structure

- `src/model/` - Data models (User, Task)
- `src/dbase/` - Database repositories and connection
- `src/User_int/` - CLI interface
- `tests/` - Unit tests

## Task Model

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

