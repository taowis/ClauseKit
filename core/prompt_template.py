import os

def load_prompt_template(language: str = "en") -> str:
    """
    Load a prompt template based on the specified language.

    Args:
        language (str): Language code ("en" or "zh").

    Returns:
        str: The content of the prompt template.
    """
    prompt_dir = os.path.join(os.path.dirname(__file__), "..", "prompts")

    if language.lower() == "zh":
        prompt_file = os.path.join(prompt_dir, "chinese_prompt.txt")
    else:
        prompt_file = os.path.join(prompt_dir, "english_prompt.txt")

    try:
        with open(prompt_file, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "[Error] Prompt template not found."