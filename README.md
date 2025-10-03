# **Task_list_proj1**
### Author: Michael Sanders 

## **Project Overview**
This project is intended to build a full-stack TODO application with user authentication, tasks, and labels. The backend will be a RESTful API built with Python's FastAPI, and the frontend will be a Next.js application. The application will use MongoDB for data persistence. This project is designed to provide hands-on experience with modern web development tools and best practices.

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

## 🎯 Current Status: Phase 1 - CLI Application ✅

**Phase 1 Complete!** A fully functional Python CLI CRUD application with MongoDB integration has been implemented.

### ✅ Completed Features (Phase 1)

#### Core CRUD Operations
- ✨ **Create Tasks** - Add new tasks with all required fields
- 📖 **Read Tasks** - View all tasks or specific task by ID
- 🔄 **Update Tasks** - Modify existing task properties
- 🗑️ **Delete Tasks** - Remove individual or all tasks

#### Advanced Features
- 🔍 **Search** - Find tasks by title, description, or user
- 🎯 **Filter by Status** - View Pending, In Progress, or Completed tasks
- 🏆 **Filter by Priority** - View High, Medium, or Low priority tasks
- 🎨 **Beautiful UI** - Color-coded terminal interface using Rich library
- 📊 **Table Views** - Organized display of multiple tasks
- 📝 **Detailed Views** - Comprehensive information panels for individual tasks

#### Technical Implementation
- 🗄️ **MongoDB Integration** - Full database connectivity using PyMongo
- 🔐 **Environment Configuration** - Secure credentials using python-dotenv
- 🏗️ **Clean Architecture** - Modular structure with separation of concerns
- 🧪 **Unit Tests** - Test coverage for Task model
- 📚 **Comprehensive Documentation** - Setup guides and quick start

### 📋 Task Fields Implemented
- ✅ Title (required)
- ✅ Description (optional)
- ✅ Priority (High/Medium/Low)
- ✅ Status (Pending/In Progress/Completed)
- ✅ Due Date
- ✅ Color
- ✅ Time Unit
- ✅ Can Parallel (boolean)
- ✅ Parallel Tasks (list)
- ✅ Predecessor Task
- ✅ User Assignment
- ✅ Created/Updated Timestamps

## 🚀 Quick Start

### Installation & Setup
```bash
# Clone the repository
git clone https://github.com/mrsanders2014/Task_list_proj1.git
cd Task_list_proj1

# Install dependencies
uv sync
# or: pip install -r requirements.txt

# Configure MongoDB connection
cp env.example .env
# Edit .env with your MongoDB URL
```

### Running the Application
```bash
python main.py
```

**📚 For detailed instructions, see:**
- [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) - Complete setup guide
- [QUICK_START.md](QUICK_START.md) - Quick reference guide

## 🛠️ Technologies Used

### Current Stack (Phase 1 - CLI)
- **Python 3.12+** - Core language
- **PyMongo 4.15+** - MongoDB driver
- **Rich 14.1+** - Beautiful terminal interface
- **python-dotenv 1.1+** - Environment configuration
- **UV** - Modern Python package manager
- **MongoDB** - NoSQL database
- **pytest** - Testing framework
- **black/ruff/pylint** - Code quality tools

### Future Stack (Phase 2-3)
- **FastAPI** - RESTful API backend
- **Next.js** - Frontend framework
- **JWT** - Authentication
- **Pydantic** - Data validation

## 📁 Project Structure
```
Task_list_proj1/
├── main.py                          # Application entry point
├── src/
│   └── Task_list_proj1/
│       ├── cli.py                   # CLI interface with Rich
│       ├── model/
│       │   └── Task_class.py        # Task data model
│       ├── dbase/
│       │   ├── mongodb_client.py    # MongoDB connection
│       │   └── task_repository.py   # CRUD operations
│       └── bus_rules/               # Business logic (future)
├── tests/
│   └── test_task_model.py          # Unit tests
├── pyproject.toml                   # Project configuration
├── requirements.txt                 # Pip dependencies
├── .env                            # Environment variables (create this)
├── env.example                     # Environment template
├── SETUP_INSTRUCTIONS.md           # Detailed setup guide
├── QUICK_START.md                  # Quick reference
└── README.md                       # This file
```

## 🎨 CLI Features Demo

### Main Menu
```
╔══════════════════════════════════════╗
║   Task Management System             ║
╚══════════════════════════════════════╝

Main Menu:
  1. Create Task
  2. View All Tasks
  3. View Task by ID
  4. Update Task
  5. Delete Task
  6. Search Tasks
  7. Filter by Status
  8. Filter by Priority
  9. Delete All Tasks
  0. Exit
```

### Task Table View
- Color-coded priorities (Red/Yellow/Green)
- Status indicators (Pending/In Progress/Completed)
- Due date display
- Clean, organized layout

## 🧪 Running Tests
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src

# Run specific test file
pytest tests/test_task_model.py
```

## 🔮 Roadmap

### Phase 1: CLI Application ✅ (COMPLETED)
- [x] MongoDB connection
- [x] Task CRUD operations
- [x] Search and filter functionality
- [x] Beautiful CLI interface
- [x] Comprehensive documentation
- [x] Unit tests

### Phase 2: REST API Backend (Planned)
- [ ] FastAPI application setup
- [ ] User authentication (JWT)
- [ ] RESTful endpoints for tasks
- [ ] User management endpoints
- [ ] Label system implementation
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Integration tests

### Phase 3: Frontend Application (Planned)
- [ ] Next.js application setup
- [ ] User interface design
- [ ] Authentication flow
- [ ] Task management UI
- [ ] Label management UI
- [ ] Responsive design
- [ ] End-to-end tests

### Future Enhancements
- [ ] Task dependencies visualization
- [ ] Due date notifications
- [ ] Task templates
- [ ] Export/Import functionality
- [ ] Multi-user collaboration
- [ ] Real-time updates (WebSockets)
- [ ] Mobile application

## 🤝 Contributing
This is a learning project. Suggestions and improvements are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License
This project is designed for educational purposes and hands-on experience with modern web development tools.

## 👨‍💻 Author
**Michael Sanders**
- GitHub: [@mrsanders2014](https://github.com/mrsanders2014)
- Project: [Task_list_proj1](https://github.com/mrsanders2014/Task_list_proj1)

## 🙏 Acknowledgments
- MongoDB for excellent NoSQL database
- Rich library for beautiful CLI interfaces
- UV for modern Python package management
- Python community for amazing tools and libraries

---

**Happy Task Managing! 🎉**

