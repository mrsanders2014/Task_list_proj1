# Task Manager CLI - Usage Examples

## Table of Contents
1. [Getting Started](#getting-started)
2. [User Management](#user-management)
3. [Task Management](#task-management)
4. [Advanced Features](#advanced-features)
5. [Common Workflows](#common-workflows)

---

## Getting Started

### First Time Setup

```bash
# 1. Clone repository
git clone https://github.com/mrsanders2014/Task_list_proj1.git
cd Task_list_proj1

# 2. Setup environment
cp .env.example .env

# 3. Start MongoDB (if running locally)
mongod

# 4. Install dependencies
uv sync
# OR
pip install -r requirements.txt

# 5. Run application
python main.py
```

---

## User Management

### Example 1: Register New User

```
Welcome to Task Manager CLI

Login Menu
1. Login
2. Register New User
3. Exit

Choose an option: 2

Register New User
First Name: Alice
Last Name: Johnson
User ID: alicej
Email: alice.johnson@example.com
Password: ********
Confirm Password: ********

✓ User registered successfully! ID: 67143a5f9e1b2c3d4e5f6a7b
```

### Example 2: User Login

```
Login Menu
1. Login
2. Register New User
3. Exit

Choose an option: 1

Login
User ID: alicej
Password: ********

✓ Welcome back, Alice Johnson!
```

### Example 3: View User Profile

```
Main Menu
1. Task Management
2. User Profile
3. View Statistics
4. Logout

Choose an option: 2

User Profile
1. View Profile
2. Update Profile
3. Change Password
4. Change Status
5. Back to Main Menu

Choose an option: 1

User Profile
┌──────────────┬──────────────────────────────┐
│ Field        │ Value                        │
├──────────────┼──────────────────────────────┤
│ User ID      │ alicej                       │
│ First Name   │ Alice                        │
│ Last Name    │ Johnson                      │
│ Email        │ alice.johnson@example.com    │
│ Status       │ active                       │
│ Last Login   │ 2025-10-03 10:30:45          │
└──────────────┴──────────────────────────────┘
```

### Example 4: Update Profile

```
User Profile
1. View Profile
2. Update Profile
3. Change Password
4. Change Status
5. Back to Main Menu

Choose an option: 2

Update Profile
Leave fields empty to keep current values

First Name [Alice]: 
Last Name [Johnson]: 
Email [alice.johnson@example.com]: alice.j@company.com

✓ Profile updated successfully
```

### Example 5: Change Password

```
User Profile
Choose an option: 3

Change Password
Current Password: ********
New Password: ********
Confirm New Password: ********

✓ Password changed successfully
```

---

## Task Management

### Example 6: Create Simple Task

```
Task Management
Choose an option: 1

Create New Task
Title: Buy groceries
Description: Milk, bread, eggs, cheese
Priority (1-10, leave empty for none): 5
Due Date (YYYY-MM-DD, leave empty for none): 2025-10-04
Add labels? (y/n): n
Time unit [minutes/hours/days/weeks] (hours): hours
Estimated time (leave empty for none): 1
Status [open/inprocess/completed/deleted] (open): open
Notification time unit [minutes/hours/days/weeks] (hours): hours
Send notification before due date (leave empty for none): 2

✓ Task created successfully! ID: 67143b2a8c9d0e1f2a3b4c5d
```

### Example 7: Create Task with Labels

```
Create New Task
Title: Complete Q4 report
Description: Financial analysis and projections
Priority (1-10, leave empty for none): 9
Due Date (YYYY-MM-DD, leave empty for none): 2025-10-15
Add labels? (y/n): y

Label name: Work
Label color (hex) [#808080]: #FF5733
Add another label? (y/n): y

Label name: Urgent
Label color (hex) [#808080]: #FFC300
Add another label? (y/n): y

Label name: Finance
Label color (hex) [#808080]: #3498DB
Add another label? (y/n): n

Time unit [minutes/hours/days/weeks] (hours): days
Estimated time (leave empty for none): 3
Status [open/inprocess/completed/deleted] (open): inprocess
Notification time unit [minutes/hours/days/weeks] (hours): days
Send notification before due date (leave empty for none): 1
Add task dependencies? (y/n): n

✓ Task created successfully! ID: 67143c5d9e0f1a2b3c4d5e6f
```

### Example 8: Create Task with Dependencies

```
Create New Task
Title: Deploy application
Description: Deploy to production server
Priority (1-10, leave empty for none): 10
Due Date (YYYY-MM-DD, leave empty for none): 2025-10-10
Add labels? (y/n): y

Label name: Deployment
Label color (hex) [#808080]: #E74C3C
Add another label? (y/n): n

Time unit [minutes/hours/days/weeks] (hours): hours
Estimated time (leave empty for none): 2
Status [open/inprocess/completed/deleted] (open): open
Notification time unit [minutes/hours/days/weeks] (hours): hours
Send notification before due date (leave empty for none): 4
Add task dependencies? (y/n): y

Task ID to depend on: 67143c5d9e0f1a2b3c4d5e6f
Add another dependency? (y/n): y

Task ID to depend on: 67143b2a8c9d0e1f2a3b4c5d
Add another dependency? (y/n): n

✓ Task created successfully! ID: 67143d8f0a1b2c3d4e5f6a7b
```

### Example 9: View All Tasks

```
Task Management
Choose an option: 2

┌─────────────┬────────────────────────────────┬──────────┬────────────┬────────────┬─────────────────┐
│ ID          │ Title                          │ Priority │ Status     │ Due Date   │ Labels          │
├─────────────┼────────────────────────────────┼──────────┼────────────┼────────────┼─────────────────┤
│ 67143d8f... │ Deploy application             │ 10       │ open       │ 2025-10-10 │ Deployment      │
│ 67143c5d... │ Complete Q4 report             │ 9        │ inprocess  │ 2025-10-15 │ Work, Urgent... │
│ 67143b2a... │ Buy groceries                  │ 5        │ open       │ 2025-10-04 │ None            │
└─────────────┴────────────────────────────────┴──────────┴────────────┴────────────┴─────────────────┘
```

### Example 10: Filter Tasks by Status

```
Task Management
Choose an option: 3

View Tasks by Status
Status [open/inprocess/completed/deleted]: inprocess

Tasks - Status: inprocess
┌─────────────┬────────────────────────────────┬──────────┬────────────┬────────────┬─────────────────┐
│ ID          │ Title                          │ Priority │ Status     │ Due Date   │ Labels          │
├─────────────┼────────────────────────────────┼──────────┼────────────┼────────────┼─────────────────┤
│ 67143c5d... │ Complete Q4 report             │ 9        │ inprocess  │ 2025-10-15 │ Work, Urgent... │
└─────────────┴────────────────────────────────┴──────────┴────────────┴────────────┴─────────────────┘
```

### Example 11: Filter Tasks by Priority

```
Task Management
Choose an option: 4

View Tasks by Priority
Minimum priority [1]: 8
Maximum priority [10]: 10

Tasks - Priority: 8-10
┌─────────────┬────────────────────────────────┬──────────┬────────────┬────────────┬─────────────────┐
│ ID          │ Title                          │ Priority │ Status     │ Due Date   │ Labels          │
├─────────────┼────────────────────────────────┼──────────┼────────────┼────────────┼─────────────────┤
│ 67143d8f... │ Deploy application             │ 10       │ open       │ 2025-10-10 │ Deployment      │
│ 67143c5d... │ Complete Q4 report             │ 9        │ inprocess  │ 2025-10-15 │ Work, Urgent... │
└─────────────┴────────────────────────────────┴──────────┴────────────┴────────────┴─────────────────┘
```

### Example 12: Filter Tasks by Label

```
Task Management
Choose an option: 5

View Tasks by Label
Label name: Work

Tasks - Label: Work
┌─────────────┬────────────────────────────────┬──────────┬────────────┬────────────┬─────────────────┐
│ ID          │ Title                          │ Priority │ Status     │ Due Date   │ Labels          │
├─────────────┼────────────────────────────────┼──────────┼────────────┼────────────┼─────────────────┤
│ 67143c5d... │ Complete Q4 report             │ 9        │ inprocess  │ 2025-10-15 │ Work, Urgent... │
└─────────────┴────────────────────────────────┴──────────┴────────────┴────────────┴─────────────────┘
```

### Example 13: View Overdue Tasks

```
Task Management
Choose an option: 6

Overdue Tasks
┌─────────────┬────────────────────────────────┬──────────┬────────────┬────────────┬─────────────────┐
│ ID          │ Title                          │ Priority │ Status     │ Due Date   │ Labels          │
├─────────────┼────────────────────────────────┼──────────┼────────────┼────────────┼─────────────────┤
│ 67143b2a... │ Buy groceries                  │ 5        │ open       │ 2025-10-04 │ None            │
└─────────────┴────────────────────────────────┴──────────┴────────────┴────────────┴─────────────────┘
```

### Example 14: Update Task

```
Task Management
Choose an option: 7

Update Task

[Shows all tasks table]

Enter Task ID to update: 67143b2a8c9d0e1f2a3b4c5d

Updating task: Buy groceries
Leave fields empty to keep current values

Title [Buy groceries]: Buy groceries and prepare dinner
Description [Milk, bread, eggs, cheese]: Milk, bread, eggs, cheese, vegetables, meat
Status [open/inprocess/completed/deleted] [open]: completed

✓ Task updated successfully
```

### Example 15: Delete Task (Soft Delete)

```
Task Management
Choose an option: 8

Delete Task

[Shows all tasks table]

Enter Task ID to delete: 67143b2a8c9d0e1f2a3b4c5d

Task: Buy groceries and prepare dinner
Delete type [soft/hard] (soft): soft
Are you sure you want to soft delete this task? (y/n): y

✓ Task deleted successfully
```

### Example 16: Delete Task (Hard Delete)

```
Delete Task

Enter Task ID to delete: 67143b2a8c9d0e1f2a3b4c5d

Task: Old completed task
Delete type [soft/hard] (soft): hard
Are you sure you want to hard delete this task? (y/n): y

✓ Task deleted successfully
```

---

## Advanced Features

### Example 17: View Task Statistics

```
Main Menu
Choose an option: 3

Task Statistics
┌────────────────┬───────┐
│ Metric         │ Count │
├────────────────┼───────┤
│ Total Tasks    │ 15    │
│ Open           │ 5     │
│ In Process     │ 3     │
│ Completed      │ 6     │
│ Deleted        │ 1     │
│ Overdue        │ 2     │
└────────────────┴───────┘
```

### Example 18: Complex Task with All Features

```
Create New Task
Title: Website Redesign Project
Description: Complete redesign of company website with new branding
Priority (1-10, leave empty for none): 10
Due Date (YYYY-MM-DD, leave empty for none): 2025-11-15
Add labels? (y/n): y

Label name: Web Development
Label color (hex) [#808080]: #2ECC71
Add another label? (y/n): y

Label name: High Priority
Label color (hex) [#808080]: #E74C3C
Add another label? (y/n): y

Label name: Client Project
Label color (hex) [#808080]: #9B59B6
Add another label? (y/n): n

Time unit [minutes/hours/days/weeks] (hours): weeks
Estimated time (leave empty for none): 6
Status [open/inprocess/completed/deleted] (open): inprocess
Notification time unit [minutes/hours/days/weeks] (hours): weeks
Send notification before due date (leave empty for none): 1
Add task dependencies? (y/n): y

Task ID to depend on: 67143c5d9e0f1a2b3c4d5e6f
Add another dependency? (y/n): y

Task ID to depend on: 67143d8f0a1b2c3d4e5f6a7b
Add another dependency? (y/n): n

✓ Task created successfully! ID: 67144e9f1a2b3c4d5e6f7a8b
```

---

## Common Workflows

### Workflow 1: Daily Task Management

**Morning Routine:**
```
1. Login → View Statistics
2. View Overdue Tasks
3. View Tasks by Status (open)
4. Update high-priority tasks to "inprocess"
```

**During Work:**
```
1. Create new tasks as they come up
2. Update task statuses as work progresses
3. Mark completed tasks
```

**End of Day:**
```
1. Review tasks in "inprocess"
2. Update progress
3. Plan for next day
4. Logout
```

### Workflow 2: Project Planning

**Phase 1: Setup**
```
1. Create main project task (high priority)
2. Add relevant labels (Project, Client, etc.)
3. Set due date
4. Estimate time required
```

**Phase 2: Break Down**
```
1. Create subtasks for each phase
2. Set dependencies between tasks
3. Assign priorities
4. Set individual due dates
```

**Phase 3: Execution**
```
1. Filter tasks by project label
2. Work on tasks in dependency order
3. Update statuses as completed
4. Track overdue tasks
```

### Workflow 3: Team Collaboration (Future)

**Setup:**
```
1. Create shared project
2. Add team members
3. Assign tasks to team members
4. Set up notifications
```

**Daily Standups:**
```
1. View team task statistics
2. Review overdue tasks
3. Update task statuses
4. Reassign if needed
```

### Workflow 4: Personal Task Management

**Weekly Planning:**
```
1. Review last week's completed tasks
2. Create tasks for the week
3. Assign priorities
4. Set due dates
5. Add labels (Work, Personal, Errands)
```

**Daily Execution:**
```
1. Filter by label (e.g., "Today")
2. Sort by priority
3. Work through tasks
4. Mark as completed
```

**Weekly Review:**
```
1. View statistics
2. Archive completed tasks
3. Reschedule incomplete tasks
4. Plan next week
```

---

## Tips and Best Practices

### Task Organization

**Use Consistent Labels:**
```
Work-related: "Work", "Client", "Internal"
Personal: "Personal", "Home", "Errands"
Priority: "Urgent", "Important", "Low Priority"
Categories: "Finance", "Development", "Marketing"
```

**Priority System:**
```
10: Critical, immediate action required
7-9: High priority, complete soon
4-6: Medium priority, normal workflow
1-3: Low priority, when time allows
```

**Time Estimation:**
```
Be realistic with estimates
Break large tasks into smaller ones
Track actual time vs. estimated
Adjust future estimates based on history
```

### Dependency Management

**Good Practices:**
```
✓ Use dependencies for sequential tasks
✓ Avoid circular dependencies
✓ Keep dependency chains short
✓ Document why dependencies exist
```

**Bad Practices:**
```
✗ Too many dependencies (makes tasks blocked)
✗ Unclear dependency reasons
✗ Outdated dependencies not removed
```

### Task Descriptions

**Good Example:**
```
Title: Deploy application to production
Description: 
  1. Run all tests
  2. Create deployment branch
  3. Update version number
  4. Deploy to staging
  5. Verify staging
  6. Deploy to production
  7. Verify production
  8. Notify team
```

**Bad Example:**
```
Title: Deploy
Description: Deploy stuff
```

---

## Troubleshooting Examples

### Issue: Can't Login

**Symptoms:**
```
Login
User ID: johndoe
Password: ********

✗ Invalid credentials
```

**Solutions:**
1. Verify userid (case-sensitive)
2. Reset password through profile update
3. Check account status (active/inactive)
4. Re-register if user doesn't exist

### Issue: Task Not Showing

**Symptoms:**
```
View All Tasks
No tasks found.
```

**Possible Causes:**
1. Wrong user logged in
2. Tasks filtered by status
3. Database connection issue

**Solutions:**
1. Verify logged-in user
2. Check all status filters
3. Test database connection

### Issue: Can't Create Task

**Symptoms:**
```
✗ Task creation failed: Validation error
```

**Common Mistakes:**
1. Empty title
2. Priority outside 1-10 range
3. Invalid status value
4. Invalid date format

**Solution:**
Follow validation rules carefully

---

## Advanced Scenarios

### Scenario 1: Managing Multiple Projects

```python
# Create project labels
Project A → Label: "ProjectA", Color: #FF5733
Project B → Label: "ProjectB", Color: #3498DB
Project C → Label: "ProjectC", Color: #2ECC71

# View tasks for specific project
Task Management → View Tasks by Label → "ProjectA"

# Track project progress
Main Menu → View Statistics (per project)
```

### Scenario 2: Sprint Planning

```python
# Week 1: Create all sprint tasks
Sprint Label: "Sprint-Oct-W1"
Mark high-priority tasks
Set due dates for end of sprint

# During Sprint: Daily updates
Update status: open → inprocess → completed
Track overdue tasks daily

# Sprint Review:
Filter by sprint label
View completed vs. total
Carry over incomplete tasks to next sprint
```

### Scenario 3: Recurring Tasks

```python
# Current: Create manually each time
# Future: Template system
# Workaround: Export completed task details and reuse
```

---

## Keyboard Shortcuts & Navigation Tips

### Quick Navigation
- Always read menu numbers carefully
- Use numeric input for speed
- Keep task IDs in clipboard for quick access
- Use consistent naming for easy filtering

### Efficiency Tips
1. **Batch Operations**: Create multiple similar tasks in one session
2. **Label Consistency**: Use same label names across tasks
3. **Regular Updates**: Update task statuses frequently
4. **Weekly Reviews**: Review and clean up tasks weekly
5. **Use Filters**: Master filtering to find tasks quickly

---

## Integration Examples (Future)

### Email Integration
```
Receive task notification via email
Reply to email to update task status
Forward emails to create tasks
```

### Calendar Integration
```
Sync due dates with Google Calendar
Show tasks in calendar view
Set reminders
```

### Webhook Integration
```
POST webhook on task completion
Trigger CI/CD on deployment tasks
Notify Slack on high-priority tasks
```

---

## Conclusion

This examples document provides comprehensive usage scenarios for the Task Manager CLI. Start with simple tasks and gradually use more advanced features as you become comfortable with the system.

For more information, see:
- [README.md](README.md) - Full documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick setup guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Implementation details

