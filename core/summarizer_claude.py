import os
import anthropic

# Load API key from environment
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Initialize the Claude client
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def query_claude(prompt: str, model: str = "claude-3-sonnet-20240229") -> str:
    """
    Query Anthropic Claude model to generate contract summary.

    Args:
        prompt (str): Input text prompt (usually long contract text).
        model (str): Claude model to use (default: claude-3-sonnet-20240229).

    Returns:
        str: Claude's response (summary).
    """
    try:
        response = client.messages.create(
            model=model,
            max_tokens=2048,
            temperature=0.4,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text.strip()
    except Exception as e:
        return f"[Claude API Error] {str(e)}"