import requests

def query_ollama(prompt: str, model: str = "mistral") -> str:
    """
    Query a local LLM served via Ollama REST API.

    Args:
        prompt (str): The input text prompt.
        model (str): The local model to use, e.g., "mistral", "llama3", "yi".

    Returns:
        str: Response from the local model.
    """
    try:
        response = requests.post(
            url="http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.exceptions.RequestException as e:
        return f"[Local model error] {str(e)}"