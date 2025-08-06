from core.summarizer_openai import query_openai
from core.summarizer_claude import query_claude
from core.summarizer_local import query_ollama

# core/llm_selector.py

def call_model(prompt: str, model_choice: str = "gpt-4") -> str:
    """
    Dispatch the prompt to the selected LLM.

    Args:
        prompt (str): The input text to summarize or analyze.
        model_choice (str): One of "gpt-3.5", "gpt-4", "claude-3-sonnet", "mistral", "llama3", "yi", "gemma", "phi"

    Returns:
        str: The model's response
    """
    # Alias for newer OpenAI models
    if model_choice.startswith("gpt"):
        from core.summarizer_openai import query_openai

        # Normalize OpenAI models to API-compatible aliases
        openai_model_map = {
            "gpt-3.5": "gpt-3.5-turbo",
            "gpt-4": "gpt-4",
            "gpt-4.1-mini": "gpt-4-1106-preview",
        }
        actual_model = openai_model_map.get(model_choice)
        if not actual_model:
            raise ValueError(f"❌ Unknown OpenAI model '{model_choice}'")
        return query_openai(prompt, actual_model)

    elif model_choice.startswith("claude"):
        from core.summarizer_claude import query_claude
        return query_claude(prompt, model_choice)

    elif model_choice in ["mistral", "llama3", "yi", "gemma", "phi"]:
        from core.summarizer_local import query_ollama
        return query_ollama(prompt, model_choice)

    else:
        raise ValueError(f"❌ Unsupported model choice: {model_choice}")