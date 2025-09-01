
import os
from dotenv import load_dotenv
import sys

# --- Gemini bits (commented out) ---

import sys
import requests

def main():
    if len(sys.argv) < 2:
        print("Error: No prompt provided. Usage: python main.py <prompt>")
        sys.exit(1)
    user_prompt = sys.argv[1]
    verbose = False
    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        verbose = True

    ollama_url = "http://localhost:11434/api/generate"
    model = "llama3"  # Change to your local model name
    payload = {
        "model": model,
        "prompt": user_prompt,
        "stream": False
    }
    try:
        response = requests.post(ollama_url, json=payload)
        response.raise_for_status()
        data = response.json()
        print(data.get("response", "No response from OLLAMA."))
    except Exception as e:
        print(f"Error connecting to OLLAMA: {e}")

if __name__ == "__main__":
    main()

    # --- OLLAMA logic ---
    ollama_url = "http://localhost:11434/api/generate"
    model = "llama3"  # Change to your local model name
    payload = {
        "model": model,
        "prompt": user_prompt,
        "stream": False
    }
    try:
        response = requests.post(ollama_url, json=payload)
        response.raise_for_status()
        data = response.json()
        print(data.get("response", "No response from OLLAMA."))
    except Exception as e:
        print(f"Error connecting to OLLAMA: {e}")

if __name__ == "__main__":
    main()
