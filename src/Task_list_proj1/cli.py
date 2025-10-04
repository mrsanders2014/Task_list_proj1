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

from .model.user import User
from .model.task import Task, Label
from .dbase.user_repository import UserRepository
from .dbase.task_repository import TaskRepository
from .dbase.connection import get_db_connection


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
        userid = Prompt.ask("User ID")
        password = Prompt.ask("Password", password=True)
        
        user = self.user_repo.authenticate(userid, password)
        if user:
            if user.status == "inactive":
                console.print("[red]Your account is inactive. Please contact administrator.[/red]")
                return
            
            self.current_user = user
            console.print(f"[green]✓ Welcome back, {user.firstname} {user.lastname}![/green]")
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
                firstname=firstname,
                lastname=lastname,
                userid=userid,
                email=email,
                password=password,
                status="active"
            )
            
            user_id = self.user_repo.create(user)
            console.print(f"[green]✓ User registered successfully! ID: {user_id}[/green]")
            
        except ValueError as e:
            console.print(f"[red]✗ Validation error: {e}[/red]")
        except Exception as e:
            console.print(f"[red]✗ Registration failed: {e}[/red]")
    
    def show_main_menu(self):
        """Display main menu after login."""
        console.print(f"\n[bold cyan]Logged in as: {self.current_user.firstname} {self.current_user.lastname}[/bold cyan]")
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
            
            task = Task(
                user_id=self.current_user.userid,
                title=title,
                description=description,
                priority=priority,
                due_date=due_date,
                labels=labels,
                time_unit=time_unit,
                estimated_time=estimated_time,
                status=status,
                notification_time_unit=notification_time_unit,
                notification_when=notification_when,
                dependencies=dependencies
            )
            
            task_id = self.task_repo.create(task)
            console.print(f"[green]✓ Task created successfully! ID: {task_id}[/green]")
            
        except ValueError as e:
            console.print(f"[red]✗ Validation error: {e}[/red]")
        except Exception as e:
            console.print(f"[red]✗ Task creation failed: {e}[/red]")
    
    def view_all_tasks(self):
        """View all tasks for the current user."""
        tasks = self.task_repo.get_by_user(self.current_user.userid)
        self._display_tasks(tasks, "All Tasks")
    
    def view_tasks_by_status(self):
        """View tasks filtered by status."""
        status = Prompt.ask(
            "Status",
            choices=["open", "inprocess", "completed", "deleted"]
        )
        tasks = self.task_repo.get_by_user(self.current_user.userid, status=status)
        self._display_tasks(tasks, f"Tasks - Status: {status}")
    
    def view_tasks_by_priority(self):
        """View tasks filtered by priority range."""
        min_priority = int(Prompt.ask("Minimum priority", default="1"))
        max_priority = int(Prompt.ask("Maximum priority", default="10"))
        tasks = self.task_repo.get_by_priority(
            self.current_user.userid,
            min_priority,
            max_priority
        )
        self._display_tasks(tasks, f"Tasks - Priority: {min_priority}-{max_priority}")
    
    def view_tasks_by_label(self):
        """View tasks filtered by label."""
        label_name = Prompt.ask("Label name")
        tasks = self.task_repo.get_by_label(self.current_user.userid, label_name)
        self._display_tasks(tasks, f"Tasks - Label: {label_name}")
    
    def view_overdue_tasks(self):
        """View overdue tasks."""
        tasks = self.task_repo.get_overdue_tasks(self.current_user.userid)
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
            priority = str(task.priority) if task.priority else "None"
            due_date = task.due_date.strftime("%Y-%m-%d") if task.due_date else "None"
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
        
        if task.user_id != self.current_user.userid:
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
            choices=["open", "inprocess", "completed", "deleted"],
            default=task.status
        )
        if status != task.status:
            update_data["status"] = status
        
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
        
        if task.user_id != self.current_user.userid:
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
                success = self.task_repo.soft_delete(task_id)
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
        
        table.add_row("User ID", self.current_user.userid)
        table.add_row("First Name", self.current_user.firstname)
        table.add_row("Last Name", self.current_user.lastname)
        table.add_row("Email", self.current_user.email)
        table.add_row("Status", self.current_user.status)
        table.add_row("Last Login", str(self.current_user.last_login))
        
        console.print(table)
    
    def update_profile(self):
        """Update user profile."""
        console.print("\n[bold]Update Profile[/bold]")
        console.print("Leave fields empty to keep current values\n")
        
        update_data = {}
        
        firstname = Prompt.ask("First Name", default=self.current_user.firstname)
        if firstname != self.current_user.firstname:
            update_data["firstname"] = firstname
        
        lastname = Prompt.ask("Last Name", default=self.current_user.lastname)
        if lastname != self.current_user.lastname:
            update_data["lastname"] = lastname
        
        email = Prompt.ask("Email", default=self.current_user.email)
        if email != self.current_user.email:
            update_data["email"] = email
        
        if update_data:
            success = self.user_repo.update(self.current_user.userid, update_data)
            if success:
                # Refresh current user
                self.current_user = self.user_repo.get_by_userid(self.current_user.userid)
                console.print("[green]✓ Profile updated successfully[/green]")
            else:
                console.print("[red]✗ Profile update failed[/red]")
        else:
            console.print("[yellow]No changes made[/yellow]")
    
    def change_password(self):
        """Change user password."""
        console.print("\n[bold]Change Password[/bold]")
        
        current_password = Prompt.ask("Current Password", password=True)
        if current_password != self.current_user.password:
            console.print("[red]✗ Incorrect current password[/red]")
            return
        
        new_password = Prompt.ask("New Password", password=True)
        confirm_password = Prompt.ask("Confirm New Password", password=True)
        
        if new_password != confirm_password:
            console.print("[red]✗ Passwords do not match[/red]")
            return
        
        if len(new_password) < 6:
            console.print("[red]✗ Password must be at least 6 characters[/red]")
            return
        
        success = self.user_repo.update(self.current_user.userid, {"password": new_password})
        if success:
            self.current_user.password = new_password
            console.print("[green]✓ Password changed successfully[/green]")
        else:
            console.print("[red]✗ Password change failed[/red]")
    
    def change_user_status(self):
        """Change user status."""
        console.print("\n[bold]Change Status[/bold]")
        
        status = Prompt.ask(
            "New Status",
            choices=["active", "inactive"],
            default=self.current_user.status
        )
        
        if status != self.current_user.status:
            success = self.user_repo.change_status(self.current_user.userid, status)
            if success:
                self.current_user.status = status
                console.print("[green]✓ Status changed successfully[/green]")
            else:
                console.print("[red]✗ Status change failed[/red]")
        else:
            console.print("[yellow]No change made[/yellow]")
    
    def view_statistics(self):
        """View task statistics for the current user."""
        console.print("\n[bold]Task Statistics[/bold]")
        
        stats = self.task_repo.get_task_statistics(self.current_user.userid)
        
        table = Table(box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="white")
        
        table.add_row("Total Tasks", str(stats.get("total", 0)))
        table.add_row("Open", str(stats.get("open", 0)))
        table.add_row("In Process", str(stats.get("inprocess", 0)))
        table.add_row("Completed", str(stats.get("completed", 0)))
        table.add_row("Deleted", str(stats.get("deleted", 0)))
        table.add_row("Overdue", str(stats.get("overdue", 0)))
        
        console.print(table)
    
    def logout(self):
        """Log out the current user."""
        console.print(f"[cyan]Goodbye, {self.current_user.firstname}![/cyan]")
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
