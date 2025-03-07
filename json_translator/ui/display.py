"""Display utilities for JSON Translator."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

# Initialize console
console = Console(width=100, highlight=True)


def display_app_header():
    """Display the application header."""
    title = "[bold green]🌐 JSON Translator[/bold green]"
    header_text = Text.from_markup(
        "[bold blue]JSON Translation Tool[/bold blue]\n\n"
        "[cyan]Translate your JSON language files using Google Translate API[/cyan]\n"
        "[dim]Supports multiple language codes and preserves JSON structure[/dim]"
    )
    
    header = Panel(
        header_text,
        border_style="green",
        box=box.DOUBLE,
        title=title
    )
    console.print(header)
    console.print()


def display_comparison(original, translated, title="Translation Results"):
    """Display a side-by-side comparison of original and translated text, including nested objects.
    
    Args:
        original (dict): Original JSON data
        translated (dict): Translated JSON data
        title (str): Title for the comparison table
    """
    table = Table(title=title, box=box.ROUNDED, expand=True)
    table.add_column("Key Path", style="cyan", no_wrap=True)
    table.add_column("Original (English)", style="green")
    table.add_column("Translated", style="yellow")

    # Function to flatten nested dictionaries with path information
    def flatten_dict(d, parent_key=''):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    # Flatten both dictionaries
    flat_original = flatten_dict(original)
    flat_translated = flatten_dict(translated)
    
    # Add rows to the table
    for key in flat_original.keys():
        if key in flat_translated:
            table.add_row(key, str(flat_original[key]), str(flat_translated[key]))

    console.print(table)


def display_available_languages(languages):
    """Display a table of available languages.
    
    Args:
        languages (list): List of language codes
    """
    from json_translator.utils.language_utils import get_language_name
    
    table = Table(title="Available Language Codes", box=box.ROUNDED)
    table.add_column("Code", style="cyan")
    table.add_column("Language", style="green")
    
    for code in languages:
        table.add_row(code, get_language_name(code))
        
    console.print(table)


def display_translation_sample(data, translations, sample_size=3):
    """Display a sample of translations for each language.
    
    Args:
        data (dict): Original data
        translations (dict): Dictionary of translated data by language code
        sample_size (int): Number of items to show in the sample
    """
    from json_translator.utils.language_utils import get_language_name
    
    console.print()
    
    # For each language, show a sample comparison
    for lang, translated_data in translations.items():
        # For nested structures, we'll show a sample of flattened keys
        def flatten_dict(d, parent_key=''):
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}.{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(flatten_dict(v, new_key).items())
                else:
                    items.append((new_key, v))
            return dict(items)
        
        flat_data = flatten_dict(data)
        flat_translated = flatten_dict(translated_data)
        
        sample_size = min(sample_size, len(flat_data))
        sample_keys = list(flat_data.keys())[:sample_size]
        
        # Create sample dictionaries for display
        # We need to reconstruct nested dictionaries from the flattened keys
        sample_original = {}
        sample_translated = {}
        
        for key in sample_keys:
            parts = key.split('.')
            
            # Build the nested structure for original data
            current = sample_original
            for i, part in enumerate(parts[:-1]):
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = flat_data[key]
            
            # Build the nested structure for translated data
            current = sample_translated
            for i, part in enumerate(parts[:-1]):
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = flat_translated[key]
        
        language_name = get_language_name(lang)
        
        display_comparison(
            sample_original, 
            sample_translated, 
            f"{language_name} ({lang}) Preview ({sample_size} of {len(flat_data)} items)"
        )
        console.print()


def display_success_message(saved_files):
    """Display a success message with the list of saved files.
    
    Args:
        saved_files (list): List of saved file paths
    """
    if saved_files:
        files_list = "\n".join([f"[bold cyan]- {file}[/bold cyan]" for file in saved_files])
        console.print(Panel(
            f"[bold green]✓[/bold green] Translations successfully saved to:\n\n{files_list}",
            border_style="green",
            title="Success"
        )) 