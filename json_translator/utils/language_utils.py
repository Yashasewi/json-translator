"""Language utilities for JSON Translator."""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Initialize console
console = Console(width=100, highlight=True)


def get_language_name(code):
    """Get the full name of a language from its code.
    
    Args:
        code (str): Language code
        
    Returns:
        str: Full language name
    """
    language_names = {
        "en": "English",
        "id": "Bahasa Indonesia",
        "ms": "Bahasa Melayu",
        "cs": "Čeština",
        "da": "Dansk",
        "de": "Deutsch",
        "es": "Español",
        "fil": "Filipino",
        "fr": "Français",
        "hr": "Hrvatski",
        "it": "Italiano",
        "nl": "Nederlands",
        "no": "Norsk",
        "pl": "Polski",
        "pt": "Português",
        "pt-BR": "Português (Brasileiro)",
        "ro": "Romanian",
        "sr": "Србија",
        "ru": "Русский",
        "fi": "Suomi",
        "sv": "Svenska",
        "tr": "Türkçe",
        "vi": "Tiếng Việt",
        "th": "ไทย",
        "el": "Ελληνικά",
        "ko": "한국어",
        "ja": "日本語",
        "zh": "中文",
        "zh-TW": "繁體中文",
        "ar": "Arabic",
        "hi": "Hindi",
    }
    return language_names.get(code, f"Language code: {code}")


def is_valid_language_code(code):
    """Check if a language code is valid for Google Translate API.
    
    Args:
        code (str): Language code to check
        
    Returns:
        bool: True if valid, False otherwise
    """
    valid_languages = {
        "en", "id", "ms", "cs", "da", "de", "es", "fil", "fr", "hr", "it",
        "nl", "no", "pl", "pt", "pt-BR", "ro", "sr", "ru", "fi", "sv", "tr",
        "vi", "th", "el", "ko", "ja", "zh", "zh-TW", "ar", "hi"
        # Add more language codes as needed
    }
    return code in valid_languages


def get_available_languages():
    """Return a list of available language codes.
    
    Returns:
        list: List of supported language codes
    """
    return [
        "en", "id", "ms", "cs", "da", "de", "es", "fil", "fr", "hr", "it",
        "nl", "no", "pl", "pt", "pt-BR", "ro", "sr", "ru", "fi", "sv", "tr",
        "vi", "th", "el", "ko", "ja", "zh", "zh-TW", "ar", "hi"
    ]


def display_language_info(target_languages):
    """Display information about the target languages.
    
    Args:
        target_languages (list or str): Target language code(s)
    """
    # Convert to list if it's a string
    if isinstance(target_languages, str):
        target_languages = [target_languages]
    
    languages_info = []
    for lang in target_languages:
        language_name = get_language_name(lang)
        languages_info.append(f"[bold]{language_name}[/bold] ({lang})")
    
    info_panel = Panel(
        f"[bold]Target Languages:[/bold] {', '.join(languages_info)}",
        title="Language Information",
        border_style="blue"
    )
    console.print(info_panel)


def validate_language_codes(target_languages):
    """Validate language codes and return valid ones.
    
    Args:
        target_languages (list): List of language codes to validate
        
    Returns:
        tuple: (valid_languages, invalid_languages)
    """
    valid_languages = []
    invalid_languages = []
    
    for lang in target_languages:
        if is_valid_language_code(lang):
            valid_languages.append(lang)
        else:
            invalid_languages.append(lang)
            console.print(f"[bold yellow]Warning:[/bold yellow] Invalid language code: {lang}. Skipping.")
    
    if invalid_languages:
        console.print(Panel(
            f"[bold yellow]The following language codes are invalid and will be skipped:[/bold yellow]\n{', '.join(invalid_languages)}",
            border_style="yellow",
            title="Warning"
        ))
    
    if not valid_languages:
        console.print(Panel(
            "[bold red]No valid language codes provided.[/bold red]\nPlease use --list-languages to see available codes.",
            border_style="red",
            title="Error"
        ))
    
    return valid_languages, invalid_languages 