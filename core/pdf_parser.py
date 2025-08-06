import fitz  # PyMuPDF

def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract raw text from a Streamlit UploadedFile object using PyMuPDF.
    
    Args:
        uploaded_file (UploadedFile): The uploaded PDF file.

    Returns:
        str: Extracted plain text.
    """
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text