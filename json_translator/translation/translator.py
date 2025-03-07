"""Translation functionality for JSON Translator."""

import copy
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TaskProgressColumn
from google.cloud import translate_v2 as translate

# Initialize console
console = Console(width=100, highlight=True)


def translate_json(data, target_languages, api_key=None):
    """Translate all values in a JSON dictionary to multiple languages, including nested objects.
    
    Args:
        data (dict): JSON data to translate
        target_languages (list or str): Target language code(s)
        api_key (str, optional): Google Translate API key
        
    Returns:
        dict: Dictionary of translated data by language code
    """
    # Convert single language to list for consistent handling
    if isinstance(target_languages, str):
        target_languages = [target_languages]
    
    # Configure the client
    if api_key:
        try:
            from googleapiclient.discovery import build
            service = build('translate', 'v2', developerKey=api_key)
            use_api_key = True
            console.print("[bold green]✓[/bold green] Using Google Translate API with provided key")
        except ImportError:
            console.print(Panel("[bold yellow]Warning:[/bold yellow] googleapiclient not installed. Falling back to application default credentials.", 
                               border_style="yellow", title="Warning"))
            client = translate.Client()
            use_api_key = False
    else:
        client = translate.Client()
        use_api_key = False
        console.print("[bold blue]ℹ[/bold blue] Using Google Cloud application default credentials")
    
    # Extract all translatable strings from the JSON (including nested objects)
    texts_to_translate = []
    text_paths = []
    
    def extract_texts(obj, path=[]):
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_path = path + [key]
                if isinstance(value, (dict, list)):
                    extract_texts(value, new_path)
                elif isinstance(value, str):
                    texts_to_translate.append(value)
                    text_paths.append(new_path)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_path = path + [i]
                if isinstance(item, (dict, list)):
                    extract_texts(item, new_path)
                elif isinstance(item, str):
                    texts_to_translate.append(item)
                    text_paths.append(new_path)
    
    extract_texts(data)
    
    # Create a deep copy of the original data to modify for each language
    translations = {lang: copy.deepcopy(data) for lang in target_languages}
    
    # Track progress with enhanced progress bar
    with Progress(
        SpinnerColumn(style="green"),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=40, complete_style="green", finished_style="green"),
        TaskProgressColumn(),
        TextColumn("[bold]{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
        expand=True
    ) as progress:
        # Create a task for each language
        tasks = {
            lang: progress.add_task(
                f"[bold green]Translating to {lang}...", 
                total=len(texts_to_translate)
            ) for lang in target_languages
        }

        # Process each language
        for target_language in target_languages:
            # Batch translate for efficiency (100 at a time)
            batch_size = 100
            for i in range(0, len(texts_to_translate), batch_size):
                batch = texts_to_translate[i : i + batch_size]
                try:
                    if use_api_key:
                        result = service.translations().list(
                            q=batch,
                            target=target_language,
                            source='en'
                        ).execute()
                        
                        translations_result = result.get('translations', [])
                        
                        # Store results
                        for j, translation in enumerate(translations_result):
                            index = i + j
                            path = text_paths[index]
                            
                            # Navigate to the correct position in the translated_data
                            target = translations[target_language]
                            for p in path[:-1]:
                                target = target[p]
                            
                            # Update the value
                            target[path[-1]] = translation['translatedText']
                    else:
                        results = client.translate(
                            batch, target_language=target_language, source_language="en"
                        )
                        
                        # Store results
                        for j, result in enumerate(results):
                            index = i + j
                            path = text_paths[index]
                            
                            # Navigate to the correct position in the translated_data
                            target = translations[target_language]
                            for p in path[:-1]:
                                target = target[p]
                            
                            # Update the value
                            target[path[-1]] = result["translatedText"]

                    # Update progress bar for this language
                    progress.update(tasks[target_language], advance=len(batch))

                except Exception as e:
                    console.print(Panel(f"[bold red]Translation error for {target_language}:[/bold red] {str(e)}", 
                                       border_style="red", title="Error"))
                    # Continue with other languages instead of exiting
                    translations.pop(target_language, None)
                    break

    return translations 