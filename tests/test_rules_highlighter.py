import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from core.rules_highlighter import load_termination_rules, apply_rules

SAMPLE_CONTRACT = """
This is a sample rental agreement.
Either party may terminate the lease with 14 days notice.
The tenant must pay rent on time.
The landlord may enter the premises with notice.
"""

def test_termination_rule_matches():
    rules = load_termination_rules()
    results = apply_rules(SAMPLE_CONTRACT, rules)

    assert isinstance(results, list)
    assert any("14 days notice" in r["description"] for r in results)

def test_apply_rules_returns_highlight_spans():
    rules = load_termination_rules()
    results = apply_rules(SAMPLE_CONTRACT, rules)

    for match in results:
        assert "start" in match
        assert "end" in match
        assert "description" in match
