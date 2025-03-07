"""Command-line interface for JSON Translator."""

import argparse
import os
import sys
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.text import Text

from json_translator.utils.language_utils import (
    get_available_languages,
    validate_language_codes,
    display_language_info
)
from json_translator.ui.display import display_available_languages

# Initialize console
console = Console(width=100, highlight=True)


def parse_arguments():
    """Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Translate JSON language files to multiple languages")
    parser.add_argument("--input", help="Input JSON file path")
    parser.add_argument("--output", help="Output directory path for translated files")
    parser.add_argument("--key", help="Google Translate API Key")
    parser.add_argument("--target", help="Target language codes (comma-separated, e.g., fr,es,de)")
    parser.add_argument("--list-languages", action="store_true", help="List available language codes and exit")

    return parser.parse_args()


def handle_list_languages_option(args):
    """Handle the --list-languages option.
    
    Args:
        args (argparse.Namespace): Parsed arguments
        
    Returns:
        bool: True if the option was handled and the program should exit
    """
    if args.list_languages:
        available_languages = get_available_languages()
        display_available_languages(available_languages)
        return True
    return False


def get_input_file(args):
    """Get the input file path from arguments or prompt the user.
    
    Args:
        args (argparse.Namespace): Parsed arguments
        
    Returns:
        str: Input file path
    """
    input_file = args.input or Prompt.ask(
        Text("Enter input JSON file path", style="bold cyan")
    )

    if not os.path.exists(input_file):
        console.print(Panel(f"[bold red]Error:[/bold red] File '{input_file}' not found", 
                           border_style="red", title="File Error"))
        sys.exit(1)
        
    return input_file


def get_target_languages(args):
    """Get target languages from arguments or prompt the user.
    
    Args:
        args (argparse.Namespace): Parsed arguments
        
    Returns:
        list: List of valid target language codes
    """
    available_languages = get_available_languages()
    
    if args.target:
        target_languages = args.target.split(',')
    else:
        # Multi-select language prompt
        console.print(Text("\nAvailable languages:", style="bold cyan"))
        console.print(f"  0. [bold green]All languages[/bold green]")
        for i, lang in enumerate(available_languages):
            console.print(f"  {i+1}. {lang}")
        
        language_input = Prompt.ask(
            Text("\nEnter target language codes (comma-separated), numbers from the list, or 0 for all languages", style="bold cyan"),
            default="fr"
        )
        
        # Process the input - handle both language codes and numbers
        target_languages = []
        for item in [lang.strip() for lang in language_input.split(',')]:
            # Check if the input is "0" for all languages
            if item == "0":
                target_languages = available_languages.copy()
                break
            # Check if the input is a number
            elif item.isdigit():
                index = int(item) - 1  # Convert to 0-based index
                if 0 <= index < len(available_languages):
                    target_languages.append(available_languages[index])
                else:
                    console.print(f"[bold yellow]Warning:[/bold yellow] Invalid language number: {item}. Skipping.")
            else:
                target_languages.append(item)
        
        if not target_languages:
            target_languages = ["fr"]  # Default to French if no valid languages
    
    # Validate language codes
    valid_languages, _ = validate_language_codes(target_languages)
    
    if not valid_languages:
        sys.exit(1)
        
    return valid_languages


def get_api_key(args):
    """Get the API key from arguments, environment, or prompt the user.
    
    Args:
        args (argparse.Namespace): Parsed arguments
        
    Returns:
        str or None: API key or None if using application default credentials
    """
    api_key = args.key or os.environ.get("GOOGLE_TRANSLATE_API_KEY")
    
    if not api_key:
        api_key = Prompt.ask(
            Text("Enter Google Translate API key", style="bold cyan"),
            password=True,
            default="",
        )
        
    # Check for credentials file
    has_credentials_file = "GOOGLE_APPLICATION_CREDENTIALS" in os.environ
    if has_credentials_file and not api_key:
        credentials_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
        if os.path.exists(credentials_path):
            console.print(Panel(f"[bold green]Using Google Application Credentials[/bold green]\nPath: {credentials_path}", 
                               border_style="green", title="Authentication"))
            
    return api_key


def get_output_directory(args):
    """Get the output directory from arguments or prompt the user.
    
    Args:
        args (argparse.Namespace): Parsed arguments
        
    Returns:
        str: Output directory path
    """
    if args.output:
        output_dir = args.output
    else:
        output_dir = Prompt.ask(
            Text("Enter output directory path", style="bold cyan"),
            default="translations"
        )
        
    return output_dir


def confirm_save_translations(output_dir):
    """Ask the user to confirm saving translations.
    
    Args:
        output_dir (str): Output directory path
        
    Returns:
        bool: True if the user confirms, False otherwise
    """
    return Confirm.ask(Text(f"Save translations to {output_dir}?", style="bold cyan")) 