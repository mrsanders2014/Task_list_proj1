"""
CLI Interface
Command-line interface for the Task Manager application using Rich library.
"""

from datetime import datetime
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import box

from src.model.user import User
from src.model.task import Task, Label
from src.dbase.user_repository import UserRepository
from src.dbase.task_repository import TaskRepository
from src.dbase.connection import get_db_connection


console = Console()


class TaskManagerCLI:
    """Command-line interface for Task Manager."""
    
    def __init__(self):
        """Initialize CLI with repositories."""
        self.user_repo = UserRepository()
        self.task_repo = TaskRepository()
        self.current_user: Optional[User] = None
        
        # Initialize database indexes
        try:
            db_conn = get_db_connection()
            db_conn.create_indexes()
        except Exception as e:
            console.print(f"[yellow]Warning: Could not create indexes: {e}[/yellow]")
    
    def run(self):
        """Main entry point for the CLI application."""
        console.print(Panel.fit(
            "[bold cyan]Task Manager CLI[/bold cyan]\n"
            "MongoDB-based Task Management System",
            border_style="cyan"
        ))
        
        while True:
            if not self.current_user:
                self.show_login_menu()
            else:
                self.show_main_menu()
    
    def show_login_menu(self):
        """Display login/registration menu."""
        console.print("\n[bold]Login Menu[/bold]")
        console.print("1. Login")
        console.print("2. Register New User")
        console.print("3. Exit")
        
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3"])
        
        if choice == "1":
            self.login()
        elif choice == "2":
            self.register_user()
        elif choice == "3":
            console.print("[cyan]Goodbye![/cyan]")
            exit(0)
    
    def login(self):
        """Handle user login."""
        console.print("\n[bold]Login[/bold]")
        username = Prompt.ask("Username")
        password = Prompt.ask("Password", password=True)
        
        user = self.user_repo.authenticate(username, password)
        if user:
            if not user.is_active:
                console.print("[red]Your account is inactive. Please contact administrator.[/red]")
                return
            
            self.current_user = user
            console.print(f"[green]✓ Welcome back, {user.get_full_name()}![/green]")
        else:
            console.print("[red]✗ Invalid credentials[/red]")
    
    def register_user(self):
        """Handle new user registration."""
        console.print("\n[bold]Register New User[/bold]")
        
        try:
            firstname = Prompt.ask("First Name")
            lastname = Prompt.ask("Last Name")
            userid = Prompt.ask("User ID")
            email = Prompt.ask("Email")
            password = Prompt.ask("Password", password=True)
            confirm_password = Prompt.ask("Confirm Password", password=True)
            
            if password != confirm_password:
                console.print("[red]✗ Passwords do not match[/red]")
                return
            
            user = User(
                username=userid,
                email=email,
                first_name=firstname,
                last_name=lastname
            )
            
            user_id = self.user_repo.create(user)
            console.print(f"[green]✓ User registered successfully! ID: {user_id}[/green]")
            
        except ValueError as e:
            console.print(f"[red]✗ Validation error: {e}[/red]")
        except Exception as e:
            console.print(f"[red]✗ Registration failed: {e}[/red]")
    
    def show_main_menu(self):
        """Display main menu after login."""
        console.print(f"\n[bold cyan]Logged in as: {self.current_user.get_full_name()}[/bold cyan]")
        console.print("\n[bold]Main Menu[/bold]")
        console.print("1. Task Management")
        console.print("2. User Profile")
        console.print("3. View Statistics")
        console.print("4. Logout")
        
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4"])
        
        if choice == "1":
            self.task_management_menu()
        elif choice == "2":
            self.user_profile_menu()
        elif choice == "3":
            self.view_statistics()
        elif choice == "4":
            self.logout()
    
    def task_management_menu(self):
        """Display task management submenu."""
        console.print("\n[bold]Task Management[/bold]")
        console.print("1. Create New Task")
        console.print("2. View All Tasks")
        console.print("3. View Tasks by Status")
        console.print("4. View Tasks by Priority")
        console.print("5. View Tasks by Label")
        console.print("6. View Overdue Tasks")
        console.print("7. Update Task")
        console.print("8. Delete Task")
        console.print("9. Back to Main Menu")
        
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9"])
        
        if choice == "1":
            self.create_task()
        elif choice == "2":
            self.view_all_tasks()
        elif choice == "3":
            self.view_tasks_by_status()
        elif choice == "4":
            self.view_tasks_by_priority()
        elif choice == "5":
            self.view_tasks_by_label()
        elif choice == "6":
            self.view_overdue_tasks()
        elif choice == "7":
            self.update_task()
        elif choice == "8":
            self.delete_task()
    
    def create_task(self):
        """Create a new task."""
        console.print("\n[bold]Create New Task[/bold]")
        
        try:
            title = Prompt.ask("Title")
            description = Prompt.ask("Description", default="")
            
            # Priority (optional)
            priority_str = Prompt.ask("Priority (1-10, leave empty for none)", default="")
            priority = int(priority_str) if priority_str else None
            
            # Due date (optional)
            due_date_str = Prompt.ask("Due Date (YYYY-MM-DD, leave empty for none)", default="")
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d") if due_date_str else None
            
            # Labels
            labels = []
            if Confirm.ask("Add labels?", default=False):
                while True:
                    label_name = Prompt.ask("Label name")
                    label_color = Prompt.ask("Label color (hex)", default="#808080")
                    labels.append(Label(label_name, label_color))
                    if not Confirm.ask("Add another label?", default=False):
                        break
            
            # Time estimation
            time_unit = Prompt.ask(
                "Time unit",
                choices=["minutes", "hours", "days", "weeks"],
                default="hours"
            )
            estimated_time_str = Prompt.ask("Estimated time (leave empty for none)", default="")
            estimated_time = float(estimated_time_str) if estimated_time_str else None
            
            # Status
            status = Prompt.ask(
                "Status",
                choices=["open", "inprocess", "completed", "deleted"],
                default="open"
            )
            
            # Notification
            notification_time_unit = Prompt.ask(
                "Notification time unit",
                choices=["minutes", "hours", "days", "weeks"],
                default="hours"
            )
            notification_when_str = Prompt.ask(
                "Send notification before due date (leave empty for none)",
                default=""
            )
            notification_when = float(notification_when_str) if notification_when_str else None
            
            # Dependencies
            dependencies = []
            if Confirm.ask("Add task dependencies?", default=False):
                while True:
                    dep_id = Prompt.ask("Task ID to depend on")
                    dependencies.append(dep_id)
                    if not Confirm.ask("Add another dependency?", default=False):
                        break
            
            # Create task management details if any management fields are provided
            task_mgmt = None
            if priority or due_date or estimated_time:
                from src.model.task import TaskMgmtDetails
                task_mgmt = TaskMgmtDetails(
                    priority=priority if priority else 1,
                    duedate=due_date,
                    time_unit=time_unit,
                    estimated_time_to_complete=estimated_time,
                    notify_time=notification_when if notification_when else 0,
                    notify_time_units=notification_time_unit,
                    notification_wanted="Y" if notification_when else "N"
                )
            
            task = Task(
                user_id=str(self.current_user._id) if self.current_user._id else self.current_user.username,
                title=title,
                description=description,
                labels=labels,
                task_mgmt=task_mgmt,
                status=status.capitalize() if status == "open" else status
            )
            
            task_id = self.task_repo.create(task)
            console.print(f"[green]✓ Task created successfully! ID: {task_id}[/green]")
            
        except ValueError as e:
            console.print(f"[red]✗ Validation error: {e}[/red]")
        except Exception as e:
            console.print(f"[red]✗ Task creation failed: {e}[/red]")
    
    def view_all_tasks(self):
        """View all tasks for the current user."""
        user_id = str(self.current_user._id) if self.current_user._id else self.current_user.username
        tasks = self.task_repo.get_by_user(user_id)
        self._display_tasks(tasks, "All Tasks")
    
    def view_tasks_by_status(self):
        """View tasks filtered by status."""
        status = Prompt.ask(
            "Status",
            choices=["Created", "Started", "InProcess", "Modified", "Scheduled", "Complete", "Deleted"]
        )
        user_id = str(self.current_user._id) if self.current_user._id else self.current_user.username
        tasks = self.task_repo.get_by_user(user_id, status=status)
        self._display_tasks(tasks, f"Tasks - Status: {status}")
    
    def view_tasks_by_priority(self):
        """View tasks filtered by priority range."""
        min_priority = int(Prompt.ask("Minimum priority", default="1"))
        max_priority = int(Prompt.ask("Maximum priority", default="10"))
        user_id = str(self.current_user._id) if self.current_user._id else self.current_user.username
        tasks = self.task_repo.get_by_priority(
            user_id,
            min_priority,
            max_priority
        )
        self._display_tasks(tasks, f"Tasks - Priority: {min_priority}-{max_priority}")
    
    def view_tasks_by_label(self):
        """View tasks filtered by label."""
        label_name = Prompt.ask("Label name")
        user_id = str(self.current_user._id) if self.current_user._id else self.current_user.username
        tasks = self.task_repo.get_by_label(user_id, label_name)
        self._display_tasks(tasks, f"Tasks - Label: {label_name}")
    
    def view_overdue_tasks(self):
        """View overdue tasks."""
        user_id = str(self.current_user._id) if self.current_user._id else self.current_user.username
        tasks = self.task_repo.get_overdue_tasks(user_id)
        self._display_tasks(tasks, "Overdue Tasks")
    
    def _display_tasks(self, tasks: List[Task], title: str):
        """Display tasks in a formatted table."""
        if not tasks:
            console.print(f"[yellow]No tasks found.[/yellow]")
            return
        
        table = Table(title=title, box=box.ROUNDED)
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="white")
        table.add_column("Priority", style="yellow")
        table.add_column("Status", style="green")
        table.add_column("Due Date", style="magenta")
        table.add_column("Labels", style="blue")
        
        for task in tasks:
            task_id = str(task._id) if task._id else "N/A"
            priority = str(task.task_mgmt.priority) if task.task_mgmt else "None"
            due_date = task.task_mgmt.duedate.strftime("%Y-%m-%d") if task.task_mgmt and task.task_mgmt.duedate else "None"
            labels = ", ".join([label.name for label in task.labels]) if task.labels else "None"
            
            table.add_row(
                task_id[:8] + "...",
                task.title[:30],
                priority,
                task.status,
                due_date,
                labels[:20]
            )
        
        console.print(table)
    
    def update_task(self):
        """Update an existing task."""
        console.print("\n[bold]Update Task[/bold]")
        
        # First, show all tasks
        self.view_all_tasks()
        
        task_id = Prompt.ask("Enter Task ID to update")
        task = self.task_repo.get_by_id(task_id)
        
        if not task:
            console.print("[red]✗ Task not found[/red]")
            return
        
        user_id = str(self.current_user._id) if self.current_user._id else self.current_user.username
        if task.user_id != user_id:
            console.print("[red]✗ You don't have permission to update this task[/red]")
            return
        
        console.print(f"\nUpdating task: {task.title}")
        console.print("Leave fields empty to keep current values\n")
        
        update_data = {}
        
        # Update fields
        title = Prompt.ask("Title", default=task.title)
        if title != task.title:
            update_data["title"] = title
        
        description = Prompt.ask("Description", default=task.description)
        if description != task.description:
            update_data["description"] = description
        
        status = Prompt.ask(
            "Status",
            choices=["Created", "Started", "InProcess", "Modified", "Scheduled", "Complete", "Deleted"],
            default=task.status
        )
        if status != task.status:
            reason = Prompt.ask("Reason for status change", default="User updated")
            success = self.task_repo.update_status(task_id, status, reason)
            if success:
                console.print("[green]✓ Task status updated successfully[/green]")
                return
            else:
                console.print("[red]✗ Task status update failed[/red]")
                return
        
        if update_data:
            success = self.task_repo.update(task_id, update_data)
            if success:
                console.print("[green]✓ Task updated successfully[/green]")
            else:
                console.print("[red]✗ Task update failed[/red]")
        else:
            console.print("[yellow]No changes made[/yellow]")
    
    def delete_task(self):
        """Delete a task."""
        console.print("\n[bold]Delete Task[/bold]")
        
        # Show all tasks first
        self.view_all_tasks()
        
        task_id = Prompt.ask("Enter Task ID to delete")
        task = self.task_repo.get_by_id(task_id)
        
        if not task:
            console.print("[red]✗ Task not found[/red]")
            return
        
        user_id = str(self.current_user._id) if self.current_user._id else self.current_user.username
        if task.user_id != user_id:
            console.print("[red]✗ You don't have permission to delete this task[/red]")
            return
        
        console.print(f"\nTask: {task.title}")
        
        delete_type = Prompt.ask(
            "Delete type",
            choices=["soft", "hard"],
            default="soft"
        )
        
        if Confirm.ask(f"Are you sure you want to {delete_type} delete this task?"):
            if delete_type == "soft":
                reason = Prompt.ask("Reason for deletion", default="User deleted")
                success = self.task_repo.soft_delete(task_id, reason)
            else:
                success = self.task_repo.delete(task_id)
            
            if success:
                console.print("[green]✓ Task deleted successfully[/green]")
            else:
                console.print("[red]✗ Task deletion failed[/red]")
    
    def user_profile_menu(self):
        """Display user profile menu."""
        console.print("\n[bold]User Profile[/bold]")
        console.print("1. View Profile")
        console.print("2. Update Profile")
        console.print("3. Change Password")
        console.print("4. Change Status")
        console.print("5. Back to Main Menu")
        
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5"])
        
        if choice == "1":
            self.view_profile()
        elif choice == "2":
            self.update_profile()
        elif choice == "3":
            self.change_password()
        elif choice == "4":
            self.change_user_status()
    
    def view_profile(self):
        """View current user profile."""
        console.print("\n[bold]User Profile[/bold]")
        
        table = Table(box=box.ROUNDED)
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Username", self.current_user.username)
        table.add_row("First Name", self.current_user.first_name or "N/A")
        table.add_row("Last Name", self.current_user.last_name or "N/A")
        table.add_row("Email", self.current_user.email)
        table.add_row("Status", "Active" if self.current_user.is_active else "Inactive")
        table.add_row("Last Login", str(self.current_user.last_login) if self.current_user.last_login else "Never")
        
        console.print(table)
    
    def update_profile(self):
        """Update user profile."""
        console.print("\n[bold]Update Profile[/bold]")
        console.print("Leave fields empty to keep current values\n")
        
        update_data = {}
        
        firstname = Prompt.ask("First Name", default=self.current_user.first_name or "")
        if firstname and firstname != self.current_user.first_name:
            update_data["first_name"] = firstname
        
        lastname = Prompt.ask("Last Name", default=self.current_user.last_name or "")
        if lastname and lastname != self.current_user.last_name:
            update_data["last_name"] = lastname
        
        email = Prompt.ask("Email", default=self.current_user.email)
        if email != self.current_user.email:
            update_data["email"] = email
        
        if update_data:
            success = self.user_repo.update(self.current_user.username, update_data)
            if success:
                # Refresh current user
                self.current_user = self.user_repo.get_by_username(self.current_user.username)
                console.print("[green]✓ Profile updated successfully[/green]")
            else:
                console.print("[red]✗ Profile update failed[/red]")
        else:
            console.print("[yellow]No changes made[/yellow]")
    
    def change_password(self):
        """Change user password."""
        console.print("\n[bold]Change Password[/bold]")
        console.print("[yellow]Password management is not implemented in this version.[/yellow]")
        console.print("[yellow]Please use external authentication system.[/yellow]")
    
    def change_user_status(self):
        """Change user status."""
        console.print("\n[bold]Change Account Status[/bold]")
        
        current_status = "active" if self.current_user.is_active else "inactive"
        new_status = Prompt.ask(
            "New Status",
            choices=["active", "inactive"],
            default=current_status
        )
        
        is_active = (new_status == "active")
        
        if is_active != self.current_user.is_active:
            success = self.user_repo.change_status(self.current_user.username, is_active)
            if success:
                self.current_user.is_active = is_active
                console.print("[green]✓ Status changed successfully[/green]")
            else:
                console.print("[red]✗ Status change failed[/red]")
        else:
            console.print("[yellow]No change made[/yellow]")
    
    def view_statistics(self):
        """View task statistics for the current user."""
        console.print("\n[bold]Task Statistics[/bold]")
        
        user_id = str(self.current_user._id) if self.current_user._id else self.current_user.username
        stats = self.task_repo.get_task_statistics(user_id)
        
        table = Table(box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="white")
        
        table.add_row("Total Tasks", str(stats.get("total", 0)))
        table.add_row("Created", str(stats.get("Created", 0)))
        table.add_row("Started", str(stats.get("Started", 0)))
        table.add_row("In Process", str(stats.get("InProcess", 0)))
        table.add_row("Modified", str(stats.get("Modified", 0)))
        table.add_row("Scheduled", str(stats.get("Scheduled", 0)))
        table.add_row("Complete", str(stats.get("Complete", 0)))
        table.add_row("Deleted", str(stats.get("Deleted", 0)))
        table.add_row("Overdue", str(stats.get("overdue", 0)))
        
        console.print(table)
    
    def logout(self):
        """Log out the current user."""
        console.print(f"[cyan]Goodbye, {self.current_user.get_full_name()}![/cyan]")
        self.current_user = None


def main():
    """Main entry point for CLI application."""
    try:
        cli = TaskManagerCLI()
        cli.run()
    except KeyboardInterrupt:
        console.print("\n[cyan]Application interrupted. Goodbye![/cyan]")
    except Exception as e:
        console.print(f"[red]Fatal error: {e}[/red]")
        raise
