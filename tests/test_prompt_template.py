import pytest
from core.prompt_template import load_prompt_template

def test_load_english_prompt():
    prompt = load_prompt_template(language="en")
    assert isinstance(prompt, str)
    assert "residential tenancy" in prompt.lower()
    assert "{text}" in prompt

def test_load_chinese_prompt():
    prompt = load_prompt_template(language="zh")
    assert isinstance(prompt, str)
    assert "新南威尔士州" in prompt or "合同原文" in prompt
    assert "{text}" in prompt

def test_invalid_language_defaults_to_english():
    prompt = load_prompt_template(language="fr")
    assert isinstance(prompt, str)
    assert "residential tenancy" in prompt.lower()  # fallback to English