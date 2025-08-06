import pytest
from core.llm_selector import call_model
from core.prompt_template import load_prompt_template

# Mock contract text
SAMPLE_CONTRACT = """
This Residential Tenancy Agreement is between John Smith (Landlord) and Jane Doe (Tenant).
The property is located at 123 Main Street, Sydney NSW.
The lease begins on 1 July 2025 and ends on 30 June 2026.
The weekly rent is $600, paid every Friday.
A bond of $2,400 is required.
Early termination requires 14 days notice and may incur a break fee.
"""

def test_prompt_template_loading():
    prompt = load_prompt_template(language="en")
    assert "{text}" in prompt
    assert "residential tenancy agreements" in prompt.lower()

def test_call_model_openai(monkeypatch):
    # Monkeypatch OpenAI call to simulate return
    def mock_openai(prompt):
        return "Mock summary from GPT-4"

    monkeypatch.setattr("core.llm_selector.query_openai", mock_openai)

    prompt_template = load_prompt_template(language="en")
    full_prompt = prompt_template.replace("{text}", SAMPLE_CONTRACT)
    summary = call_model(full_prompt, model_choice="gpt-4")

    assert isinstance(summary, str)
    assert "Mock summary" in summary