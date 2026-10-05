# Code Comment Generator

A Streamlit application that uses a local Ollama model to add clear,
descriptive comments to source code. Paste code or upload a file, select its
language, generate a commented version, and download the result.

## Features

- Supports Python, JavaScript, TypeScript, Java, C++, C#, Go, and Ruby
- Uploads source files or accepts pasted code
- Detects the language from uploaded file extensions
- Adds module, class, function, block, and line comments
- Preserves the original code structure in the generated response
- Shows syntax-highlighted output with line numbers
- Downloads the commented code with the correct file extension
- Limits submissions to 20,000 characters
- Removes Markdown code fences returned by the model
- Displays useful errors when Ollama is unavailable or times out
- Uses a configurable light theme and editor-style two-panel layout

## Requirements

- Python 3.10 or newer
- [Ollama](https://ollama.com/) installed and running
- An Ollama model, such as `llama3`

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/code-comment-generator.git
cd code-comment-generator
```

### 2. Create and activate a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Ollama and download a model

```bash
ollama serve
ollama pull llama3
```

If Ollama is already running as a desktop service, only the `ollama pull`
command may be needed.

### 5. Create your local configuration

Copy the example configuration:

```bash
cp config.example.py config.py
```

`config.py` is ignored by Git and must not be uploaded if it contains private
or machine-specific settings.

The default local configuration is:

```python
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3:latest"
REQUEST_TIMEOUT_SECONDS = 90
MAX_CODE_CHARS = 20_000
```

You can also override the URL and model with environment variables:

```bash
export OLLAMA_URL="http://localhost:11434/api/generate"
export OLLAMA_MODEL="llama3:latest"
```

### 6. Run the application

```bash
streamlit run app.py
```

The application normally opens at <http://localhost:8501>.

## Project structure

```text
.
├── app.py                         # Application entry point
├── config.example.py              # Safe configuration template
├── config.py                      # Local configuration; ignored by Git
├── requirements.txt               # Python dependencies
├── services/
│   ├── __init__.py
│   └── ollama.py                  # Prompt and Ollama API logic
├── ui/
│   ├── __init__.py
│   └── app.py                     # Streamlit interface
├── .streamlit/
│   └── config.toml                # Theme and widget styling
├── .gitignore                     # Excludes local/private files
└── Code Comment .code-workspace   # Optional VS Code workspace file
```

## How it works

1. The UI accepts pasted code or an uploaded file.
2. The selected or detected language is included in the prompt.
3. `services/ollama.py` sends the prompt to the configured Ollama endpoint.
4. The response is cleaned and displayed in the output panel.
5. The result can be downloaded using the matching source-code extension.

The application does not use a hosted AI API. Code is sent to the Ollama
endpoint configured in your local `config.py`.

## GitHub and private files

The following files and folders should not be uploaded:

```text
config.py
.venv/
__pycache__/
.DS_Store
```

They are already listed in `.gitignore`.

The following files are safe and useful to upload:

```text
app.py
ui/
services/
config.example.py
.streamlit/config.toml
README.md
requirements.txt
.gitignore
```

