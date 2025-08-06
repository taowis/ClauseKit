import pytest
from core import summarizer_claude

SAMPLE_PROMPT = """
You are a legal assistant. Please summarize the following contract:
Contract Text: The lease starts on 1 July 2025 and ends on 30 June 2026.
"""

def test_query_claude_success(monkeypatch):
    """
    Simulates a successful response from the Claude API.
    """
    def mock_query(prompt):
        return "Mocked Claude summary."

    monkeypatch.setattr(summarizer_claude, "query_claude", mock_query)

    result = summarizer_claude.query_claude(SAMPLE_PROMPT)
    assert isinstance(result, str)
    assert "Mocked Claude" in result

def test_query_claude_error(monkeypatch):
    """
    Simulates a failure or exception during Claude API call.
    """
    def mock_query(prompt):
        raise Exception("Simulated Claude failure")

    monkeypatch.setattr(summarizer_claude, "query_claude", mock_query)

    with pytest.raises(Exception) as exc_info:
        summarizer_claude.query_claude(SAMPLE_PROMPT)

    assert "Simulated Claude failure" in str(exc_info.value)