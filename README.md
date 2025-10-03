# **Task_list_proj1**
### Author: Michael Sanders 

## **Project Overview**
This project is a Python CLI-based Task Management application with MongoDB integration. It provides comprehensive CRUD operations for managing users and tasks, featuring user authentication, task categorization with labels, priority management, dependency tracking, and rich CLI interface powered by the Rich library.

## Included Features: 


### User Management
    
    Account creation by a user designed to create/manage task lists.
    Login capability so that a user profile and tasks can be managed (including deletion)
    Ensure proper 'logout' capability to ensure security of users data.

### Task Management
    Be able create a new task, be able to assign priority, start/stop date and predecessor task
    Be able to view all existing tasks in various sort form
    Be able to update an existing task on every field with certain exceptions
    Be able to delete a task

### Labeling System
    Be able tocreate and manage labels (e.g., 'Work,' 'Personal,' 'Urgent'), so I can categorize and/or prioritize my tasks.
    Be able to assign one or more labels to a task, so I can easily filter and organize my tasks.

### Required Task Fields: Every task must include a 
- title 
- optional description 
- priority level (e.g., High, Medium, Low)
- task color
- deadline (due-date)
- time unit for task
- task status
- can task be done in parallel with other tasks?
- if so, list of parallel tasks
- predecessor task


### Data Persistence
    The application must persist all user, task, and label data in a MongoDB database.

### Possible Goals as of 10/1/25

    As a user, I want to filter my tasks by label, so I can quickly find and organize what I need to work on.
    As a user, I want to be able to edit my profile details, so I can keep my information up to date.
    As a user, I want the application to be responsive and work well on different screen sizes, so I can access my tasks from any device, including my phone or tablet.
    As a user, I want to see clear, helpful messages when something goes wrong, so I know what happened and how to proceed.

### Technical Requirements & File Structure
Use best python practices for project structure
Will include the use UV project management

### Database: MongoDB
The project should leverage a MongoDB database filled with appropriately modeled documents & collections. 
Initial design will consist of a database with 2 collections: Users and Tasks. Tasks will be related to Users (1 user -> many tasks)

### Backend: FastAPI
The project directory will follow a modular structure based on current Python best practices. 

### Frontend: Next.js
The project structure should follow best practices for a Next.js application. 



### GitHubRepository Location/URL
   [Task_list_proj1](https://github.com/mrsanders2014/Task_list_proj1)

## **Technical Build and Run Instructions**

### Prerequisites
- Python 3.12 or higher
- MongoDB instance (local or remote)
- UV package manager (recommended) or pip

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mrsanders2014/Task_list_proj1.git
   cd Task_list_proj1
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and configure your MongoDB connection:
   ```
   project_db_url=mongodb://localhost:27017/
   DATABASE_NAME=task_manager
   ```

3. **Install dependencies:**
   
   Using UV (recommended):
   ```bash
   uv sync
   ```
   
   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

### MongoDB Setup

Ensure MongoDB is running on your system:

**Local MongoDB:**
```bash
mongod
```

**Or use MongoDB Atlas** (cloud-hosted) and update the `project_db_url` in `.env` accordingly.

### Project Structure
```
Task_list_proj1/
├── src/
│   └── Task_list_proj1/
│       ├── model/           # Data models (User, Task, Label)
│       ├── dbase/           # Database layer (connection, repositories)
│       ├── bus_rules/       # Business rules (future expansion)
│       └── cli.py           # CLI interface
├── tests/                   # Test files
├── main.py                  # Application entry point
├── pyproject.toml           # Project configuration
├── .env                     # Environment variables (not in git)
└── README.md
```

## **Technologies Used**
- **Python 3.12+**: Core programming language
- **MongoDB**: NoSQL database for data persistence
- **PyMongo**: MongoDB driver for Python
- **Rich**: Beautiful terminal interface library
- **python-dotenv**: Environment variable management
- **UV**: Modern Python package manager

## **Implemented Features**

### User Management ✓
- User registration with validation
- Secure login/logout functionality
- User profile management (view, update)
- Password management
- Account status control (active/inactive)
- Last login tracking

### Task Management ✓
- Create tasks with comprehensive attributes:
  - Title and description
  - Priority levels (1-10)
  - Due dates
  - Custom labels with colors
  - Time estimation (with units: minutes, hours, days, weeks)
  - Task status (open, inprocess, completed, deleted)
  - Notification settings
  - Task dependencies
- View tasks with multiple filters:
  - All tasks
  - By status
  - By priority range
  - By label
  - Overdue tasks
- Update tasks
- Delete tasks (soft delete and hard delete)

### Labeling System ✓
- Create multiple labels per task
- Custom label colors (hex format)
- Filter tasks by label
- Visual label representation in CLI

### Task Dependencies ✓
- Link tasks to other tasks
- Create dependency lists
- Track task relationships

### Data Persistence ✓
- MongoDB integration with proper indexing
- Users collection with unique userid and email
- Tasks collection with proper relationships
- Optimized queries for filtering and sorting

### Statistics & Reporting ✓
- Task count by status
- Overdue task tracking
- User activity monitoring

## **Usage Examples**

### Registering a New User
1. Run the application
2. Select "Register New User"
3. Enter your details (firstname, lastname, userid, email, password)
4. Login with your credentials

### Creating a Task
1. Login to your account
2. Navigate to "Task Management" → "Create New Task"
3. Fill in task details:
   - Title (required)
   - Description (optional)
   - Priority (1-10, optional)
   - Due date (YYYY-MM-DD format, optional)
   - Labels (multiple, with colors)
   - Time estimation
   - Dependencies (other task IDs)

### Viewing Tasks
- View all tasks
- Filter by status (open, inprocess, completed, deleted)
- Filter by priority range
- Filter by label name
- View overdue tasks

## **Data Models**

### User Collection
```json
{
  "_id": "ObjectId",
  "firstname": "string",
  "lastname": "string",
  "userid": "string (unique)",
  "email": "string (unique)",
  "password": "string",
  "status": "active|inactive",
  "last_login": "datetime"
}
```

### Tasks Collection
```json
{
  "_id": "ObjectId",
  "user_id": "string (references Users.userid)",
  "title": "string",
  "description": "string",
  "priority": "integer (1-10, optional)",
  "due_date": "datetime (optional)",
  "labels": [
    {
      "name": "string",
      "color": "string (hex)"
    }
  ],
  "time_unit": "minutes|hours|days|weeks",
  "estimated_time": "float (optional)",
  "status": "open|inprocess|completed|deleted",
  "notification_time_unit": "minutes|hours|days|weeks",
  "notification_when": "float (optional)",
  "dependencies": ["task_id", "task_id"],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## **Future Enhancements**
- RESTful API with FastAPI
- Next.js frontend
- Task notifications
- Task scheduling
- Collaboration features
- Export/Import functionality
- Data visualization and analytics

