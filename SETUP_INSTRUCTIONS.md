# Task Management CLI - Setup Instructions

## Overview
A Python CLI CRUD application for managing tasks with MongoDB integration. Built with PyMongo, Rich for beautiful terminal UI, and python-dotenv for environment configuration.

## Features
- ✨ Beautiful CLI interface with Rich library
- 📝 Full CRUD operations (Create, Read, Update, Delete)
- 🔍 Search and filter capabilities
- 🎨 Color-coded priority and status indicators
- 🗄️ MongoDB integration
- 📊 Detailed task views with all fields

## Prerequisites
- Python 3.12 or higher
- MongoDB instance (local or remote)
- UV package manager (or pip)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/mrsanders2014/Task_list_proj1.git
cd Task_list_proj1
```

### 2. Install Dependencies
Using UV (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root based on the `env.example` template:

```bash
cp env.example .env
```

Edit the `.env` file with your MongoDB connection details:
```env
project_db_url=mongodb://localhost:27017/
DATABASE_NAME=task_list_db
COLLECTION_NAME=tasks
```

**MongoDB Connection Options:**
- Local: `mongodb://localhost:27017/`
- Atlas: `mongodb+srv://username:password@cluster.mongodb.net/`
- With auth: `mongodb://username:password@localhost:27017/`

### 4. Start MongoDB
Make sure your MongoDB instance is running:

**Local MongoDB:**
```bash
# Linux/Mac
sudo systemctl start mongod

# Windows (if installed as service)
net start MongoDB

# Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

**MongoDB Atlas:**
- Create a free cluster at [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
- Get your connection string and update `.env`

## Running the Application

### Using Python directly:
```bash
python main.py
```

### Using UV:
```bash
uv run python main.py
```

## Usage Guide

### Main Menu Options:
1. **Create Task** - Add a new task with all details
2. **View All Tasks** - Display all tasks in a table
3. **View Task by ID** - Show detailed information for a specific task
4. **Update Task** - Modify an existing task
5. **Delete Task** - Remove a specific task
6. **Search Tasks** - Search by title, description, or user
7. **Filter by Status** - Show tasks with specific status (Pending/In Progress/Completed)
8. **Filter by Priority** - Show tasks with specific priority (High/Medium/Low)
9. **Delete All Tasks** - Remove all tasks (with confirmation)
0. **Exit** - Quit the application

### Task Fields:
- **Title** (required): Task name
- **Description** (optional): Detailed description
- **Priority** (required): High, Medium, or Low
- **Status** (required): Pending, In Progress, or Completed
- **Due Date** (optional): Deadline in YYYY-MM-DD format
- **Color** (optional): Visual indicator
- **Time Unit** (optional): Time estimate unit
- **Can Parallel** (optional): Whether task can run in parallel
- **Parallel Tasks** (optional): List of related parallel task IDs
- **Predecessor Task** (optional): ID of task that must complete first
- **User** (optional): Assigned user

## Project Structure
```
Task_list_proj1/
├── main.py                          # Application entry point
├── src/
│   └── Task_list_proj1/
│       ├── __init__.py
│       ├── cli.py                   # CLI interface with Rich
│       ├── model/
│       │   ├── __init__.py
│       │   └── Task_class.py        # Task data model
│       ├── dbase/
│       │   ├── __init__.py
│       │   ├── mongodb_client.py    # MongoDB connection handler
│       │   └── task_repository.py   # CRUD operations
│       └── bus_rules/
│           └── __init__.py
├── tests/
│   └── __init__.py
├── pyproject.toml                   # Project configuration
├── .env                             # Environment variables (create this)
└── env.example                      # Environment template
```

## Troubleshooting

### MongoDB Connection Issues
**Error:** "Error connecting to MongoDB"
- Verify MongoDB is running: `mongosh` or `mongo`
- Check connection string in `.env`
- Ensure firewall allows port 27017
- For Atlas, check IP whitelist

### Module Import Errors
**Error:** "ModuleNotFoundError"
```bash
# Install dependencies
uv sync
# or
pip install pymongo python-dotenv rich
```

### Permission Issues
**Error:** "Permission denied"
```bash
# Linux/Mac - fix MongoDB data directory
sudo chown -R $(whoami) /data/db
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
# Format code
black src/

# Check types
mypy src/

# Lint code
pylint src/
ruff check src/
```

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `project_db_url` | MongoDB connection string | `mongodb://localhost:27017/` |
| `DATABASE_NAME` | Database name | `task_list_db` |
| `COLLECTION_NAME` | Collection name for tasks | `tasks` |

## Support & Contribution
- GitHub: [Task_list_proj1](https://github.com/mrsanders2014/Task_list_proj1)
- Author: Michael Sanders
- Issues: Please report bugs via GitHub Issues

## License
This project is designed for educational purposes and hands-on experience with modern web development tools.

## Next Steps
This CLI serves as the foundation for the full-stack application. Future enhancements include:
- User authentication
- Label system
- FastAPI REST API backend
- Next.js frontend
- Advanced filtering and sorting
- Task dependencies visualization

