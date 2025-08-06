import os
import pytest
from core import doc_generator

SUMMARY_TEXT = """
Parties:
- Landlord: John Smith
- Tenant: Jane Doe

Property Address:
- 123 Example Street, Sydney NSW

Lease Period:
- Start: 1 July 2025
- End: 30 June 2026

Rent and Bond:
- Weekly Rent: $600
- Bond: $2400
"""

def test_export_to_pdf(tmp_path):
    output_path = tmp_path / "summary.pdf"
    doc_generator.export_to_pdf(str(output_path), SUMMARY_TEXT)
    assert output_path.exists()
    assert output_path.stat().st_size > 0

#def test_export_to_docx(tmp_path):
#    output_path = tmp_path / "summary.docx"
#    doc_generator.export_to_docx(str(output_path), SUMMARY_TEXT)
#    assert output_path.exists()
#    assert output_path.stat().st_size > 0

def test_export_to_html(tmp_path):
    output_path = tmp_path / "summary.html"
    doc_generator.export_to_html(str(output_path), SUMMARY_TEXT, model="GPT-4", timestamp="2025-08-02 14:00")
    assert output_path.exists()
    assert output_path.stat().st_size > 0
