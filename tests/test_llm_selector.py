import pytest
from core import llm_selector

SAMPLE_PROMPT = "Summarize the lease terms from this contract..."

#def test_call_model_openai(monkeypatch):
#    def mock_query_openai(prompt):
#        return "Mock GPT summary"
#    monkeypatch.setattr(llm_selector, "query_openai", mock_query_openai)

#    result = llm_selector.call_model(SAMPLE_PROMPT, model_choice="gpt-4")
#    assert isinstance(result, str)
#    assert "Mock GPT" in result

#def test_call_model_claude(monkeypatch):
#    def mock_query_claude(prompt):
#        return "Mock Claude summary"
#    monkeypatch.setattr(llm_selector, "query_claude", mock_query_claude)

#    result = llm_selector.call_model(SAMPLE_PROMPT, model_choice="claude-3-sonnet")
#    assert isinstance(result, str)
#    assert "Mock Claude" in result

def test_call_model_local(monkeypatch):
    def mock_query_ollama(prompt, model):
        return "Mock Local summary"

    # Patch where it's actually imported from
    monkeypatch.setattr("core.summarizer_local.query_ollama", mock_query_ollama)

    result = llm_selector.call_model(SAMPLE_PROMPT, model_choice="mistral")
    assert isinstance(result, str)
    assert "Mock Local" in result

def test_call_model_invalid_choice():
    with pytest.raises(ValueError) as exc_info:
        llm_selector.call_model(SAMPLE_PROMPT, model_choice="unknown")
    assert "Unsupported model choice" in str(exc_info.value)
