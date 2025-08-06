import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Load the OpenAI API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def query_openai(prompt: str, model: str = "gpt-4") -> str:
    """
    Calls the OpenAI Chat API with the given prompt.

    Args:
        prompt (str): The text prompt to summarize.
        model (str): OpenAI model to use. Defaults to "gpt-4".

    Returns:
        str: The summarized text output.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a legal assistant that summarizes tenancy contracts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=2048,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"[OpenAI API Error] {str(e)}"