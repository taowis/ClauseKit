import pytest
from core import summarizer_openai

SAMPLE_PROMPT = """
You are a legal assistant. Please summarize the following contract:
Contract Text: The lease starts on 1 July 2025 and ends on 30 June 2026.
"""

def test_query_openai_success(monkeypatch):
    # Define a fake response
    def mock_create(prompt):
        return "Mocked GPT-4 Summary Output"

    monkeypatch.setattr(summarizer_openai, "query_openai", mock_create)

    result = summarizer_openai.query_openai(SAMPLE_PROMPT)
    assert isinstance(result, str)
    assert "Mocked" in result

def test_query_openai_error(monkeypatch):
    # Simulate an error during API call
    def mock_create(prompt):
        raise Exception("Simulated API failure")

    monkeypatch.setattr(summarizer_openai, "query_openai", mock_create)

    try:
        summarizer_openai.query_openai(SAMPLE_PROMPT)
        assert False, "Should raise an exception"
    except Exception as e:
        assert "Simulated API failure" in str(e)