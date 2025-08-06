import pytest
from core import summarizer_local

SAMPLE_PROMPT = """
You are a legal assistant. Please summarize the following contract:
Contract Text: The lease starts on 1 July 2025 and ends on 30 June 2026.
"""

def test_query_ollama_success(monkeypatch):
    """
    Simulates a successful response from a local Ollama model.
    """
    def mock_ollama(prompt, model="mistral"):
        return "Mocked Ollama summary."

    monkeypatch.setattr(summarizer_local, "query_ollama", mock_ollama)

    result = summarizer_local.query_ollama(SAMPLE_PROMPT, model="mistral")
    assert isinstance(result, str)
    assert "Mocked Ollama" in result


def test_query_ollama_error(monkeypatch):
    """
    Simulates a failure when calling a local Ollama model.
    """
    def mock_ollama(prompt, model="mistral"):
        raise RuntimeError("Simulated Ollama error")

    monkeypatch.setattr(summarizer_local, "query_ollama", mock_ollama)

    with pytest.raises(RuntimeError) as exc_info:
        summarizer_local.query_ollama(SAMPLE_PROMPT, model="mistral")

    assert "Simulated Ollama error" in str(exc_info.value)