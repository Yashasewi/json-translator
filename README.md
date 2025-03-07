# 🌐 JSON Translator

A powerful Text User Interface (TUI) tool for translating JSON language files to multiple languages while preserving the original structure.

## 📋 Features

- Translate JSON files to multiple languages simultaneously
- Preserve nested JSON structure in translations
- Interactive TUI with rich formatting and progress indicators
- Support for Google Translate API (API key or service account)
- Preview translations before saving
- Batch processing of large JSON files
- Support for 20+ languages

## 🔧 Installation

### Prerequisites

- Python 3.6 or higher
- Google Translate API key or Google Cloud service account credentials

### Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd json-translator
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Or install the package directly:
   ```bash
   pip install .
   ```

3. Set up your Google Translate API credentials:
   - Option 1: Create a `.env` file with your API key (see `.env.example`)
   - Option 2: Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your service account JSON file

## 🚀 Usage

### Basic Usage

Run the script with no arguments for an interactive experience:

```bash
python translate_json.py
```

Or if you installed the package:

```bash
json-translator
```

The TUI will guide you through:
1. Selecting an input JSON file
2. Choosing target languages
3. Providing API credentials (if not set in environment)
4. Previewing translations
5. Saving translated files

### Command Line Arguments

```bash
python translate_json.py --input <input-file> --output <output-directory> --target <language-codes> --key <api-key>
```

Or if you installed the package:

```bash
json-translator --input <input-file> --output <output-directory> --target <language-codes> --key <api-key>
```

#### Options:

- `--input`: Path to the input JSON file
- `--output`: Directory to save translated files (default: `translations/`)
- `--target`: Comma-separated list of target language codes (e.g., `fr,es,de`)
- `--key`: Google Translate API key (optional if set in environment)
- `--list-languages`: Display available language codes and exit

### Example

```bash
python translate_json.py --input sample.json --output translations --target fr,es,de
```

## 🌍 Supported Languages

The tool supports many languages including:

- French (fr)
- Spanish (es)
- German (de)
- Italian (it)
- Japanese (ja)
- Korean (ko)
- Chinese (Simplified) (zh)
- Chinese (Traditional) (zh-TW)
- Russian (ru)
- Portuguese (pt)
- Arabic (ar)
- Hindi (hi)
- Dutch (nl)
- Swedish (sv)
- Finnish (fi)
- Danish (da)
- Norwegian (no)
- Polish (pl)
- Turkish (tr)
- Thai (th)
- Vietnamese (vi)

To see the full list of supported languages:

```bash
python translate_json.py --list-languages
```

## 📁 Input Format

The tool accepts JSON files with string values that need translation. It preserves the structure of nested objects and arrays. Example:

```json
{
    "welcome": "Welcome to our application",
    "buttons": {
        "save": "Save",
        "cancel": "Cancel"
    },
    "messages": {
        "success": "Operation completed successfully"
    }
}
```

## 🔑 API Authentication

### Option 1: API Key

1. Get a Google Translate API key from the Google Cloud Console
2. Set it in the `.env` file:
   ```
   GOOGLE_TRANSLATE_API_KEY="your-api-key-here"
   ```
   
### Option 2: Service Account

1. Create a service account in Google Cloud Console
2. Download the JSON credentials file
3. Set the environment variable:
   ```
   GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
   ```

## 📝 Notes

- The tool uses the Google Cloud Translation API, which is a paid service
- Translations are performed in batches to optimize API usage
- For large files, the tool shows progress indicators during translation

## 🛠️ Troubleshooting

- **API Authentication Errors**: Ensure your API key or service account has the Translation API enabled
- **Missing Dependencies**: Run `pip install -r requirements.txt` to install all required packages
- **Invalid Language Codes**: Use `--list-languages` to see supported language codes

## 📦 Project Structure

The project has been refactored into a modular structure:

```
json-translator/
├── json_translator/           # Main package
│   ├── __init__.py            # Package initialization
│   ├── main.py                # Main application logic
│   ├── translation/           # Translation functionality
│   │   ├── __init__.py
│   │   └── translator.py      # Translation logic
│   ├── ui/                    # User interface components
│   │   ├── __init__.py
│   │   ├── cli.py             # Command-line interface
│   │   └── display.py         # Display utilities
│   └── utils/                 # Utility functions
│       ├── __init__.py
│       ├── file_operations.py # File handling utilities
│       └── language_utils.py  # Language-related utilities
├── translate_json.py          # Entry point script
├── setup.py                   # Package setup script
├── requirements.txt           # Dependencies
├── .env.example               # Example environment variables
└── README.md                  # This file
```

## 📄 License

[MIT License](LICENSE) 