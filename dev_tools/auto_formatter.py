import os
import sys
import time
import logging
import json
import yaml
import traceback
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from subprocess import run, PIPE
from datetime import datetime

# Set up logging
log_dir = os.path.join(os.path.expanduser("~"), ".logs", "autoformatter")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "autoformatter.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Initialize Rich console for pretty printing
console = Console()


class AdvancedFormatter(FileSystemEventHandler):
    def __init__(self, watch_dir):
        self.watch_dir = watch_dir
        self.formatted_files = set()
        self.formatters = {
            ".py": self.format_python,
            ".json": self.format_json,
            ".yaml": self.format_yaml,
            ".yml": self.format_yaml,
        }
        self.stats = {"formatted": 0, "errors": 0}

    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return
        file_path = event.src_path
        _, ext = os.path.splitext(file_path)
        if ext in self.formatters and file_path not in self.formatted_files:
            self.format_file(file_path)

    def format_file(self, file_path):
        """Format a file based on its extension."""
        _, ext = os.path.splitext(file_path)
        formatter = self.formatters.get(ext)
        if formatter:
            try:
                formatter(file_path)
                self.stats["formatted"] += 1
                self.formatted_files.add(file_path)
                logging.info(f"Formatted {file_path}")
            except Exception as e:
                self.stats["errors"] += 1
                logging.error(f"Error formatting {file_path}: {str(e)}")
                logging.debug(traceback.format_exc())

    def format_python(self, file_path):
        """Format Python files using Black."""
        result = run(["black", file_path], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Black error: {result.stderr}")

    def format_json(self, file_path):
        """Format JSON files."""
        with open(file_path, "r") as f:
            data = json.load(f)
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

    def format_yaml(self, file_path):
        """Format YAML files."""
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
        with open(file_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False)


def get_watch_directory():
    """Prompt user for the directory to watch."""
    while True:
        directory = console.input(
            "[bold cyan]Enter the directory to watch (default: current directory): [/bold cyan]"
        )
        if directory == "":
            return "."
        if os.path.isdir(directory):
            return directory
        console.print("[bold red]Invalid directory. Please try again.[/bold red]")


def create_status_table(formatter):
    """Create a status table for live updates."""
    table = Table(title="Auto-formatter Status")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_row("Files Formatted", str(formatter.stats["formatted"]))
    table.add_row("Errors Encountered", str(formatter.stats["errors"]))
    table.add_row("Watch Directory", formatter.watch_dir)
    return table


def start_observer(watch_dir):
    """Start the file system observer with live updates."""
    event_handler = AdvancedFormatter(watch_dir)
    observer = Observer()
    observer.schedule(event_handler, watch_dir, recursive=True)
    observer.start()

    try:
        with Live(create_status_table(event_handler), refresh_per_second=4) as live:
            while True:
                live.update(create_status_table(event_handler))
                time.sleep(0.25)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    console.print(
        Panel.fit("[bold green]Advanced Multi-Format Auto-formatter[/bold green]")
    )
    try:
        watch_dir = get_watch_directory()
        console.print(f"[bold cyan]Watching directory: {watch_dir}[/bold cyan]")
        console.print(
            "[bold yellow]Press Ctrl+C to stop the auto-formatter.[/bold yellow]"
        )
        start_observer(watch_dir)
    except Exception as e:
        console.print("[bold red]Critical error during initialization.[/bold red]")
        console.print("[yellow]See full error details below:[/yellow]")
        console.print(traceback.format_exc())
        logging.critical(f"Critical error: {str(e)}")
        logging.debug(traceback.format_exc())
        sys.exit(1)
