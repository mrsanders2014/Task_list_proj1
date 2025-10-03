"""
CLI interface for Task Management Application
"""

from datetime import datetime
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box
from rich.text import Text

from .model.Task_class import Task
from .dbase.task_repository import TaskRepository


class TaskCLI:
    """Command Line Interface for Task Management"""
    
    def __init__(self):
        """Initialize the CLI"""
        self.console = Console()
        self.repository = TaskRepository()
        self.running = True
    
    def display_header(self):
        """Display application header"""
        header = Text("Task Management System", style="bold magenta", justify="center")
        self.console.print(Panel(header, box=box.DOUBLE, border_style="cyan"))
    
    def display_menu(self):
        """Display the main menu"""
        menu = """
[bold cyan]Main Menu:[/bold cyan]
  [green]1.[/green] Create Task
  [green]2.[/green] View All Tasks
  [green]3.[/green] View Task by ID
  [green]4.[/green] Update Task
  [green]5.[/green] Delete Task
  [green]6.[/green] Search Tasks
  [green]7.[/green] Filter by Status
  [green]8.[/green] Filter by Priority
  [green]9.[/green] Delete All Tasks
  [red]0.[/red] Exit
        """
        self.console.print(menu)
    
    def create_task(self):
        """Create a new task"""
        self.console.print("\n[bold cyan]Create New Task[/bold cyan]")
        
        try:
            title = Prompt.ask("[yellow]Title[/yellow]")
            description = Prompt.ask("[yellow]Description[/yellow] (optional)", default="")
            priority = Prompt.ask(
                "[yellow]Priority[/yellow]",
                choices=["High", "Medium", "Low"],
                default="Medium"
            )
            status = Prompt.ask(
                "[yellow]Status[/yellow]",
                choices=["Pending", "In Progress", "Completed"],
                default="Pending"
            )
            
            # Optional fields
            color = Prompt.ask("[yellow]Color[/yellow] (optional)", default="")
            time_unit = Prompt.ask("[yellow]Time Unit[/yellow] (optional)", default="")
            user = Prompt.ask("[yellow]User[/yellow] (optional)", default="")
            
            # Due date
            due_date_str = Prompt.ask(
                "[yellow]Due Date[/yellow] (YYYY-MM-DD, optional)",
                default=""
            )
            due_date = None
            if due_date_str:
                try:
                    due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
                except ValueError:
                    self.console.print("[red]Invalid date format. Skipping due date.[/red]")
            
            # Parallel tasks
            can_parallel = Confirm.ask("[yellow]Can run in parallel?[/yellow]", default=False)
            parallel_tasks = []
            if can_parallel:
                parallel_str = Prompt.ask(
                    "[yellow]Parallel tasks (comma-separated IDs)[/yellow] (optional)",
                    default=""
                )
                if parallel_str:
                    parallel_tasks = [t.strip() for t in parallel_str.split(",")]
            
            predecessor = Prompt.ask("[yellow]Predecessor task ID[/yellow] (optional)", default="")
            
            # Create task
            task = Task(
                title=title,
                description=description if description else None,
                priority=priority,
                status=status,
                due_date=due_date,
                color=color if color else None,
                time_unit=time_unit if time_unit else None,
                can_parallel=can_parallel,
                parallel_tasks=parallel_tasks if parallel_tasks else None,
                predecessor_task=predecessor if predecessor else None,
                user=user if user else None
            )
            
            task_id = self.repository.create(task)
            self.console.print(f"\n[bold green]✓ Task created successfully! ID: {task_id}[/bold green]")
            
        except Exception as e:
            self.console.print(f"[bold red]✗ Error creating task: {e}[/bold red]")
    
    def view_all_tasks(self):
        """View all tasks"""
        self.console.print("\n[bold cyan]All Tasks[/bold cyan]")
        
        try:
            tasks = self.repository.read_all()
            
            if not tasks:
                self.console.print("[yellow]No tasks found.[/yellow]")
                return
            
            self._display_tasks_table(tasks)
            
        except Exception as e:
            self.console.print(f"[bold red]✗ Error viewing tasks: {e}[/bold red]")
    
    def view_task_by_id(self):
        """View a specific task by ID"""
        self.console.print("\n[bold cyan]View Task by ID[/bold cyan]")
        
        try:
            task_id = Prompt.ask("[yellow]Task ID[/yellow]")
            task = self.repository.read(task_id)
            
            if not task:
                self.console.print(f"[red]Task with ID {task_id} not found.[/red]")
                return
            
            self._display_task_details(task)
            
        except Exception as e:
            self.console.print(f"[bold red]✗ Error viewing task: {e}[/bold red]")
    
    def update_task(self):
        """Update an existing task"""
        self.console.print("\n[bold cyan]Update Task[/bold cyan]")
        
        try:
            task_id = Prompt.ask("[yellow]Task ID[/yellow]")
            task = self.repository.read(task_id)
            
            if not task:
                self.console.print(f"[red]Task with ID {task_id} not found.[/red]")
                return
            
            self.console.print("\n[dim]Current task details:[/dim]")
            self._display_task_details(task)
            
            self.console.print("\n[dim]Leave fields empty to keep current values[/dim]")
            
            # Collect updates
            update_data = {}
            
            title = Prompt.ask(f"[yellow]Title[/yellow] (current: {task.title})", default="")
            if title:
                update_data["title"] = title
            
            description = Prompt.ask(
                f"[yellow]Description[/yellow] (current: {task.description})",
                default=""
            )
            if description:
                update_data["description"] = description
            
            priority = Prompt.ask(
                "[yellow]Priority[/yellow]",
                choices=["High", "Medium", "Low", ""],
                default=""
            )
            if priority:
                update_data["priority"] = priority
            
            status = Prompt.ask(
                "[yellow]Status[/yellow]",
                choices=["Pending", "In Progress", "Completed", ""],
                default=""
            )
            if status:
                update_data["status"] = status
            
            if update_data:
                update_data["updated_at"] = datetime.now()
                success = self.repository.update(task_id, update_data)
                
                if success:
                    self.console.print("\n[bold green]✓ Task updated successfully![/bold green]")
                else:
                    self.console.print("\n[yellow]No changes were made.[/yellow]")
            else:
                self.console.print("\n[yellow]No updates provided.[/yellow]")
                
        except Exception as e:
            self.console.print(f"[bold red]✗ Error updating task: {e}[/bold red]")
    
    def delete_task(self):
        """Delete a task"""
        self.console.print("\n[bold cyan]Delete Task[/bold cyan]")
        
        try:
            task_id = Prompt.ask("[yellow]Task ID[/yellow]")
            task = self.repository.read(task_id)
            
            if not task:
                self.console.print(f"[red]Task with ID {task_id} not found.[/red]")
                return
            
            self._display_task_details(task)
            
            confirm = Confirm.ask("\n[red]Are you sure you want to delete this task?[/red]")
            
            if confirm:
                success = self.repository.delete(task_id)
                if success:
                    self.console.print("[bold green]✓ Task deleted successfully![/bold green]")
                else:
                    self.console.print("[red]Failed to delete task.[/red]")
            else:
                self.console.print("[yellow]Deletion cancelled.[/yellow]")
                
        except Exception as e:
            self.console.print(f"[bold red]✗ Error deleting task: {e}[/bold red]")
    
    def search_tasks(self):
        """Search tasks"""
        self.console.print("\n[bold cyan]Search Tasks[/bold cyan]")
        
        try:
            query = Prompt.ask("[yellow]Search query[/yellow]")
            field = Prompt.ask(
                "[yellow]Search in field[/yellow]",
                choices=["title", "description", "user"],
                default="title"
            )
            
            tasks = self.repository.search(query, field)
            
            if not tasks:
                self.console.print(f"[yellow]No tasks found matching '{query}'.[/yellow]")
                return
            
            self.console.print(f"\n[green]Found {len(tasks)} task(s)[/green]")
            self._display_tasks_table(tasks)
            
        except Exception as e:
            self.console.print(f"[bold red]✗ Error searching tasks: {e}[/bold red]")
    
    def filter_by_status(self):
        """Filter tasks by status"""
        self.console.print("\n[bold cyan]Filter by Status[/bold cyan]")
        
        try:
            status = Prompt.ask(
                "[yellow]Status[/yellow]",
                choices=["Pending", "In Progress", "Completed"]
            )
            
            tasks = self.repository.get_by_status(status)
            
            if not tasks:
                self.console.print(f"[yellow]No tasks found with status '{status}'.[/yellow]")
                return
            
            self.console.print(f"\n[green]Found {len(tasks)} task(s)[/green]")
            self._display_tasks_table(tasks)
            
        except Exception as e:
            self.console.print(f"[bold red]✗ Error filtering tasks: {e}[/bold red]")
    
    def filter_by_priority(self):
        """Filter tasks by priority"""
        self.console.print("\n[bold cyan]Filter by Priority[/bold cyan]")
        
        try:
            priority = Prompt.ask(
                "[yellow]Priority[/yellow]",
                choices=["High", "Medium", "Low"]
            )
            
            tasks = self.repository.get_by_priority(priority)
            
            if not tasks:
                self.console.print(f"[yellow]No tasks found with priority '{priority}'.[/yellow]")
                return
            
            self.console.print(f"\n[green]Found {len(tasks)} task(s)[/green]")
            self._display_tasks_table(tasks)
            
        except Exception as e:
            self.console.print(f"[bold red]✗ Error filtering tasks: {e}[/bold red]")
    
    def delete_all_tasks(self):
        """Delete all tasks"""
        self.console.print("\n[bold red]⚠ Delete All Tasks ⚠[/bold red]")
        
        try:
            confirm = Confirm.ask(
                "[red]Are you sure you want to delete ALL tasks? This cannot be undone![/red]"
            )
            
            if confirm:
                count = self.repository.delete_all()
                self.console.print(f"[bold green]✓ Deleted {count} task(s).[/bold green]")
            else:
                self.console.print("[yellow]Deletion cancelled.[/yellow]")
                
        except Exception as e:
            self.console.print(f"[bold red]✗ Error deleting tasks: {e}[/bold red]")
    
    def _display_tasks_table(self, tasks: list):
        """Display tasks in a table format"""
        table = Table(title="Tasks", box=box.ROUNDED, show_header=True, header_style="bold cyan")
        
        table.add_column("ID", style="dim", width=24)
        table.add_column("Title", style="white", width=30)
        table.add_column("Status", width=12)
        table.add_column("Priority", width=10)
        table.add_column("Due Date", width=12)
        
        for task in tasks:
            task_id = str(task._id) if task._id else "N/A"
            
            # Color code status
            status_style = {
                "Pending": "yellow",
                "In Progress": "blue",
                "Completed": "green"
            }.get(task.status, "white")
            
            # Color code priority
            priority_style = {
                "High": "red",
                "Medium": "yellow",
                "Low": "green"
            }.get(task.priority, "white")
            
            due_date = task.due_date.strftime("%Y-%m-%d") if task.due_date else "N/A"
            
            table.add_row(
                task_id,
                task.title,
                f"[{status_style}]{task.status}[/{status_style}]",
                f"[{priority_style}]{task.priority}[/{priority_style}]",
                due_date
            )
        
        self.console.print(table)
    
    def _display_task_details(self, task: Task):
        """Display detailed information about a task"""
        details = f"""
[bold]ID:[/bold] {task._id}
[bold]Title:[/bold] {task.title}
[bold]Description:[/bold] {task.description or 'N/A'}
[bold]Status:[/bold] {task.status}
[bold]Priority:[/bold] {task.priority}
[bold]Due Date:[/bold] {task.due_date.strftime('%Y-%m-%d') if task.due_date else 'N/A'}
[bold]Color:[/bold] {task.color or 'N/A'}
[bold]Time Unit:[/bold] {task.time_unit or 'N/A'}
[bold]Can Parallel:[/bold] {task.can_parallel}
[bold]Parallel Tasks:[/bold] {', '.join(task.parallel_tasks) if task.parallel_tasks else 'N/A'}
[bold]Predecessor:[/bold] {task.predecessor_task or 'N/A'}
[bold]User:[/bold] {task.user or 'N/A'}
[bold]Created:[/bold] {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}
[bold]Updated:[/bold] {task.updated_at.strftime('%Y-%m-%d %H:%M:%S') if task.updated_at else 'N/A'}
        """
        
        self.console.print(Panel(details, title="Task Details", border_style="green"))
    
    def run(self):
        """Run the CLI application"""
        try:
            self.display_header()
            
            while self.running:
                self.display_menu()
                
                choice = Prompt.ask("\n[bold cyan]Select an option[/bold cyan]", default="0")
                
                if choice == "1":
                    self.create_task()
                elif choice == "2":
                    self.view_all_tasks()
                elif choice == "3":
                    self.view_task_by_id()
                elif choice == "4":
                    self.update_task()
                elif choice == "5":
                    self.delete_task()
                elif choice == "6":
                    self.search_tasks()
                elif choice == "7":
                    self.filter_by_status()
                elif choice == "8":
                    self.filter_by_priority()
                elif choice == "9":
                    self.delete_all_tasks()
                elif choice == "0":
                    self.console.print("\n[bold cyan]Goodbye! 👋[/bold cyan]")
                    self.running = False
                else:
                    self.console.print("[red]Invalid option. Please try again.[/red]")
                
                if self.running:
                    self.console.print("\n" + "─" * 60 + "\n")
        
        except KeyboardInterrupt:
            self.console.print("\n\n[bold cyan]Application terminated by user. Goodbye! 👋[/bold cyan]")
        except Exception as e:
            self.console.print(f"\n[bold red]✗ Fatal error: {e}[/bold red]")
        finally:
            # Clean up database connection
            try:
                self.repository.client.close()
            except Exception:
                pass


def main():
    """Main entry point for the CLI"""
    cli = TaskCLI()
    cli.run()


if __name__ == "__main__":
    main()

