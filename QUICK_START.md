# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install & Configure
```bash
# Clone the repo
git clone https://github.com/mrsanders2014/Task_list_proj1.git
cd Task_list_proj1

# Install dependencies
uv sync
# or: pip install -r requirements.txt

# Create .env file
cp env.example .env
```

### 2. Configure MongoDB
Edit `.env`:
```env
project_db_url=mongodb://localhost:27017/
DATABASE_NAME=task_list_db
COLLECTION_NAME=tasks
```

### 3. Run
```bash
python main.py
```

## 📝 Common Operations

### Create Your First Task
```
1. Select option "1" from menu
2. Enter task details:
   - Title: "Complete project documentation"
   - Description: "Write comprehensive docs"
   - Priority: "High"
   - Status: "In Progress"
   - Due Date: "2025-10-15"
```

### View All Tasks
```
Select option "2" from menu
```

### Search for a Task
```
1. Select option "6"
2. Enter search query: "documentation"
3. Choose field to search: "title"
```

### Update a Task
```
1. Select option "4"
2. Enter Task ID (from View All Tasks)
3. Update desired fields (leave empty to skip)
```

### Filter Tasks
```
By Status: Option "7" → Choose "In Progress"
By Priority: Option "8" → Choose "High"
```

## 🐳 Using Docker for MongoDB

### Quick MongoDB Setup
```bash
# Start MongoDB in Docker
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -v mongodb_data:/data/db \
  mongo:latest

# Verify it's running
docker ps

# View logs
docker logs mongodb
```

### Stop MongoDB
```bash
docker stop mongodb
```

### Restart MongoDB
```bash
docker start mongodb
```

## 🔥 MongoDB Atlas (Cloud)

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create free cluster
3. Get connection string:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/
   ```
4. Update `.env` with your connection string
5. Add your IP to Atlas IP Whitelist

## 💡 Tips

### Color-Coded Display
- **Red** = High Priority
- **Yellow** = Medium Priority / Pending Status
- **Green** = Low Priority / Completed Status
- **Blue** = In Progress Status

### Keyboard Shortcuts
- `Ctrl+C` - Exit application safely
- `Enter` - Accept default values

### Best Practices
1. Always set a due date for time-sensitive tasks
2. Use descriptive titles for easy searching
3. Update status as you progress
4. Use predecessor tasks for dependencies
5. Assign parallel tasks for concurrent work

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't connect to MongoDB | Check if MongoDB is running: `mongosh` |
| Module not found | Run `uv sync` or `pip install -r requirements.txt` |
| Permission denied | Check MongoDB data directory permissions |
| Invalid ObjectId | Make sure you're copying full Task ID |

## 📚 Example Workflow

```bash
# 1. Start the app
python main.py

# 2. Create tasks
Option 1 → Add "Design Database Schema"
Option 1 → Add "Implement API Endpoints"
Option 1 → Add "Write Unit Tests"

# 3. View your tasks
Option 2 → See all tasks in a table

# 4. Update progress
Option 4 → Update first task to "Completed"

# 5. Filter completed tasks
Option 7 → Filter by "Completed" status

# 6. Exit
Option 0 → Goodbye!
```

## 🎯 Task Management Best Practices

### Priority Guidelines
- **High**: Urgent, blocking other work, deadline today/tomorrow
- **Medium**: Important but not urgent, deadline this week
- **Low**: Nice to have, no immediate deadline

### Status Workflow
```
Pending → In Progress → Completed
```

### Using Dependencies
1. Create prerequisite task first
2. Note its ID
3. Create dependent task
4. Set predecessor_task to prerequisite's ID

## 🔗 Useful Links
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [Python dotenv](https://pypi.org/project/python-dotenv/)
- [GitHub Repository](https://github.com/mrsanders2014/Task_list_proj1)

---

**Need more help?** Check `SETUP_INSTRUCTIONS.md` for detailed information.

