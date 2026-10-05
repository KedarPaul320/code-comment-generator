import re

import requests

from config import OLLAMA_MODEL, OLLAMA_URL, REQUEST_TIMEOUT_SECONDS


def build_prompt(code: str, language: str) -> str:
    return f"""Add comments to the following {language} code:
Add clear, descriptive comments to explain exactly what each part does without making any changes to existing code lines, indentation, or overall structure.
Write a comment above the [class/function/module] that briefly explains what it does, its purpose, and its key inputs/outputs or features. Use the standard comment style for the given programming language.
For each logical block or section, add a brief block comment above it that gives an overview of what the block does.
For individual lines or statements, add short single-line comments that are direct and easy to scan.
Code:
{code}"""


def strip_code_fence(text: str) -> str:
    """Models often wrap their reply in ```lang ... ``` — strip that if present."""
    text = text.strip()
    match = re.match(r"^```[a-zA-Z0-9+\-]*\n([\s\S]*?)\n?```$", text)
    return match.group(1) if match else text


def call_ollama(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json().get("response", "")
