"""Main module for JSON Translator."""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.prompt import Confirm
from rich.text import Text

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, will use os.environ directly

from json_translator.utils.file_operations import (
    load_json_file, 
    save_json_file, 
    ensure_directory_exists
)
from json_translator.utils.language_utils import display_language_info
from json_translator.translation.translator import translate_json
from json_translator.ui.display import (
    display_app_header,
    display_comparison,
    display_translation_sample,
    display_success_message
)
from json_translator.ui.cli import (
    parse_arguments,
    handle_list_languages_option,
    get_input_file,
    get_target_languages,
    get_api_key,
    get_output_directory,
    confirm_save_translations
)

# Initialize console
console = Console(width=100, highlight=True)


def main():
    """Main function for the JSON Translator."""
    # Display app header
    display_app_header()

    # Parse command line arguments
    args = parse_arguments()

    # Handle --list-languages option
    if handle_list_languages_option(args):
        sys.exit(0)

    # Get input file
    input_file = get_input_file(args)
    
    # Load JSON with improved feedback
    with console.status("[bold blue]Loading JSON file...", spinner="dots"):
        data = load_json_file(input_file)
    
    console.print(f"[bold green]✓[/bold green] Loaded [bold]{len(data)}[/bold] translation keys from [bold cyan]{input_file}[/bold cyan]")

    # Get target languages
    target_languages = get_target_languages(args)
    
    # Display language information
    display_language_info(target_languages)

    # Get API key
    api_key = get_api_key(args)

    # Translate the JSON
    console.print()
    translations = translate_json(data, target_languages, api_key)
    console.print(f"[bold green]✓[/bold green] Translation complete! Translated to [bold]{len(translations)}[/bold] languages")

    # If no translations were successful, exit
    if not translations:
        console.print(Panel(
            "[bold red]No translations were completed successfully.[/bold red]\nPlease check your language codes and API credentials.",
            border_style="red",
            title="Error"
        ))
        sys.exit(1)

    # Show sample of translations
    display_translation_sample(data, translations)

    # Ask to view all translations
    if Confirm.ask(Text("Show detailed comparison for all languages?", style="bold cyan")):
        for lang, translated_data in translations.items():
            from json_translator.utils.language_utils import get_language_name
            language_name = get_language_name(lang)
            
            console.print()
            display_comparison(data, translated_data, f"Complete {language_name} ({lang}) Translation Results")

    # Get output directory
    console.print()
    output_dir = get_output_directory(args)
    
    # Create directory if it doesn't exist
    ensure_directory_exists(output_dir)
    
    # Save each translation to a separate file
    if confirm_save_translations(output_dir):
        with Progress(
            SpinnerColumn(style="green"),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=40),
            console=console,
        ) as progress:
            save_task = progress.add_task("[bold green]Saving translations...", total=len(translations))
            
            saved_files = []
            for lang, translated_data in translations.items():
                output_file = f"{output_dir}/translated_{lang}.json"
                success = save_json_file(translated_data, output_file)
                
                if success:
                    saved_files.append(output_file)
                
                progress.update(save_task, advance=1)
        
        display_success_message(saved_files)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print(Panel("\n[bold yellow]Translation canceled by user[/bold yellow]", 
                           border_style="yellow", title="Canceled"))
        sys.exit(0) 