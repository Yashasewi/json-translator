"""File operation utilities for JSON Translator."""

import json
import sys
import os
from rich.console import Console
from rich.panel import Panel

# Initialize console
console = Console(width=100, highlight=True)


def load_json_file(file_path):
    """Load JSON from a file.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        dict: Loaded JSON data
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        console.print(Panel(f"[bold red]Error loading JSON file:[/bold red] {str(e)}", 
                           border_style="red", title="Error"))
        sys.exit(1)


def save_json_file(data, file_path):
    """Save JSON to a file.
    
    Args:
        data (dict): JSON data to save
        file_path (str): Path to save the file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        console.print(Panel(f"[bold red]Error saving file:[/bold red] {str(e)}", 
                           border_style="red", title="Error"))
        return False


def ensure_directory_exists(directory_path):
    """Ensure that a directory exists, create it if it doesn't.
    
    Args:
        directory_path (str): Path to the directory
        
    Returns:
        bool: True if the directory exists or was created successfully
    """
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            console.print(f"[bold green]✓[/bold green] Created output directory: [bold cyan]{directory_path}[/bold cyan]")
            return True
        except Exception as e:
            console.print(Panel(f"[bold red]Error creating directory:[/bold red] {str(e)}", 
                               border_style="red", title="Error"))
            return False
    return True 