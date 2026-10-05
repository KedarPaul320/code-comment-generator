import os

# Copy this file to config.py for local settings.
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3:latest")
REQUEST_TIMEOUT_SECONDS = 90
MAX_CODE_CHARS = 20_000
