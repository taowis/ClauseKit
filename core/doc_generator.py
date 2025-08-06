from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os


def export_to_pdf(output_path, summary_text, model="Unknown", timestamp=None):
    """
    Export summary text to a formatted PDF file.

    Args:
        output_path (str): The path to the output PDF file.
        summary_text (str): The content to write into the PDF.
        model (str): The name of the model used for generation.
        timestamp (str): Timestamp of the summary generation.
    """
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica", 12)

    # Metadata header
    y = height - 40
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    c.drawString(40, y, f"📄 ClauseKit Summary Report")
    y -= 20
    c.drawString(40, y, f"Model: {model}")
    y -= 20
    c.drawString(40, y, f"Generated on: {timestamp}")
    y -= 40

    # Main summary text
    for line in summary_text.split('\n'):
        if y < 40:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 40
        c.drawString(40, y, line)
        y -= 15

    c.save()
    
    return output_path  # ✅ must return this

def export_to_html(output_path, summary_text, model="Unknown", timestamp=None):
    """
    Export summary text to an HTML file.

    Args:
        output_path (str): The path to the output HTML file.
        summary_text (str): The summary text to be embedded.
        model (str): Name of the LLM used (e.g., GPT-4).
        timestamp (str): Generation timestamp.
    """
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>ClauseKit Summary</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                line-height: 1.6;
            }}
            .header {{
                margin-bottom: 2em;
            }}
            .meta {{
                font-size: 0.9em;
                color: #555;
            }}
            .summary {{
                white-space: pre-wrap;
                background: #f9f9f9;
                padding: 1em;
                border: 1px solid #ddd;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📄 ClauseKit Summary Report</h1>
            <div class="meta">
                <p><strong>Model:</strong> {model}</p>
                <p><strong>Generated on:</strong> {timestamp}</p>
            </div>
        </div>
        <div class="summary">
            {summary_text}
        </div>
    </body>
    </html>
    """

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return output_path  # ✅ Ensure file path is returned