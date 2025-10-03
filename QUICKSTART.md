# Quick Start Guide

## Getting Started in 5 Minutes

### 1. Prerequisites Check
```bash
# Check Python version (needs 3.12+)
python --version

# Check if MongoDB is running
# If not installed, download from: https://www.mongodb.com/try/download/community
mongod --version
```

### 2. Setup Environment
```bash
# Copy environment template
cp .env.example .env

# For local MongoDB, the default settings in .env work fine:
# project_db_url=mongodb://localhost:27017/
# DATABASE_NAME=task_manager
```

### 3. Install Dependencies
```bash
# Using UV (recommended)
uv sync

# OR using pip
pip install pymongo python-dotenv rich
```

### 4. Start MongoDB
```bash
# Start MongoDB service (if not already running)
# Windows:
net start MongoDB

# Linux/Mac:
sudo systemctl start mongod
# OR
mongod
```

### 5. Run the Application
```bash
python main.py
```

## First Time Usage

### Create Your First User
1. When the app starts, select option `2` (Register New User)
2. Fill in the details:
   - First Name: `John`
   - Last Name: `Doe`
   - User ID: `johndoe`
   - Email: `john@example.com`
   - Password: `password123`

### Login
1. Select option `1` (Login)
2. Enter your User ID and Password

### Create Your First Task
1. After login, select `1` (Task Management)
2. Select `1` (Create New Task)
3. Fill in the task details:
   - Title: `Complete project documentation`
   - Description: `Write comprehensive README`
   - Priority: `8`
   - Due Date: `2025-10-15`
   - Add labels: `Yes`
     - Label name: `Work`
     - Label color: `#FF5733`
   - Time unit: `hours`
   - Estimated time: `4`
   - Status: `open`

### View Your Tasks
1. From Task Management menu, select `2` (View All Tasks)
2. You'll see a formatted table with all your tasks

## Common Operations

### Update a Task Status
1. Task Management → `7` (Update Task)
2. Enter the Task ID (first 8 characters shown in the list)
3. Change the status to `inprocess` or `completed`

### View Statistics
1. Main Menu → `3` (View Statistics)
2. See counts of tasks by status and overdue tasks

### Filter Tasks
- By Status: Task Management → `3`
- By Priority: Task Management → `4`
- By Label: Task Management → `5`
- Overdue Tasks: Task Management → `6`

## Troubleshooting

### Can't Connect to MongoDB?
- Ensure MongoDB is running: `mongod`
- Check the connection string in `.env`
- For Windows: Check if MongoDB service is running in Services

### Import Errors?
- Make sure you're in the project root directory
- Verify all dependencies are installed: `uv sync` or `pip install -r requirements.txt`

### Module Not Found?
- Ensure you're running from the project root: `python main.py`
- Check that the `src` directory structure is intact

## Environment Variables

Edit `.env` file for custom configuration:

```env
# MongoDB Connection
project_db_url=mongodb://localhost:27017/
DATABASE_NAME=task_manager

# For MongoDB Atlas (cloud):
# project_db_url=mongodb+srv://username:password@cluster.mongodb.net/

# Application Settings
APP_NAME=Task Manager CLI
DEBUG=False
```

## Example Session

```
Task Manager CLI
MongoDB-based Task Management System

Login Menu
1. Login
2. Register New User
3. Exit

Choose an option: 2

Register New User
First Name: John
Last Name: Doe
User ID: johndoe
Email: john@example.com
Password: ******
Confirm Password: ******

✓ User registered successfully! ID: 67890abcdef12345

...

✓ Welcome back, John Doe!

Logged in as: John Doe

Main Menu
1. Task Management
2. User Profile
3. View Statistics
4. Logout
```

## Tips

1. **Task IDs**: When viewing tasks, note the ID (first 8 chars) for updates/deletes
2. **Dependencies**: Use task IDs to create task dependencies
3. **Labels**: Use consistent label names for better filtering
4. **Priorities**: Use 1-10 scale (10 = highest priority)
5. **Soft Delete**: Marks task as deleted but keeps in database
6. **Hard Delete**: Permanently removes task from database

## Next Steps

- Explore all CRUD operations
- Set up task dependencies for complex workflows
- Use labels to organize tasks by categories
- Track your productivity with the statistics view
- Consider setting up MongoDB Atlas for cloud storage

For more details, see the main [README.md](README.md)

