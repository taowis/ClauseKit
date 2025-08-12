import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
from langdetect import detect
from core.prompt_template import load_prompt_template
from core.lang_selector import detect_language
from core.llm_selector import call_model
from core.doc_generator import export_to_html, export_to_pdf
from core.pdf_parser import extract_text_from_pdf  # assumed utility function
from datetime import datetime
show_advanced_models = os.getenv("SHOW_ADVANCED_MODELS", "false").lower() == "true"

# Load environment variables if any
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4.1-mini")

st.set_page_config(page_title="ClauseKitAI", layout="wide")
st.title("📄 ClauseKitAI – AI-Powered Contract Summarizer")

st.sidebar.header("⚙️ Configuration")

if show_advanced_models:
    model_choice = st.sidebar.selectbox(
        "Choose a large language model (LLM)",
        ["gpt-4.1-mini", "gpt-4", "claude", "mistral", "llama3", "yi"],
        index=["gpt-4.1-mini", "gpt-4", "claude", "mistral", "llama3", "yi"].index(DEFAULT_MODEL)
        if DEFAULT_MODEL in ["gpt-4.1-mini", "gpt-4", "claude", "mistral", "llama3", "yi"] else 0
    )
else:
    model_choice = st.sidebar.selectbox(
        "Choose a large language model (LLM)",
        ["gpt-4.1-mini", "claude"],
        index=["gpt-4.1-mini", "claude"].index(DEFAULT_MODEL)
    )

language_option = st.sidebar.selectbox(
    "Preferred language for summary",
    ["Auto Detect", "English", "Chinese"]
)

uploaded_file = st.file_uploader("Upload your legal PDF contract", type=["pdf"])

if uploaded_file is not None:
    # Step 1: Extract raw text from PDF
    raw_text = extract_text_from_pdf(uploaded_file)
    
    if not raw_text.strip():
        st.error("❌ Failed to extract text from the PDF.")
        st.stop()
    
    st.success("✅ Contract text extracted successfully.")
    st.text_area("📃 Extracted Text Preview", raw_text[:2000], height=200)

    # Step 2: Detect language
    if language_option == "Auto Detect":
        lang_code = detect_language(raw_text)
    else:
        lang_code = "zh" if language_option == "Chinese" else "en"

    st.info(f"🌐 Language selected: {'中文' if lang_code == 'zh' else 'English'}")

    # Step 3: Load prompt
    prompt_template = load_prompt_template(lang_code)
    final_prompt = prompt_template.replace("{text}", raw_text)

    # Step 4: Generate summary
    with st.spinner(f"💬 Generating summary using {model_choice}..."):
        summary_output = call_model(final_prompt, model_choice)

    st.markdown("### 🧠 AI-Generated Summary")
    st.markdown(summary_output)

    # Step 5: Export options
    col1, col2 = st.columns(2)

    with col1:
        try:
            html_file_path = export_to_html("summary.html", summary_output, model=model_choice)
            with open(html_file_path, "rb") as f:
                st.download_button("⬇️ Download HTML", f, file_name="summary.html", mime="text/html")
        except Exception as e:
            st.error(f"❌ Failed to export HTML summary.\n\n{e}")

    with col2:
        try:
            pdf_file_path = export_to_pdf("summary.pdf", summary_output)
            with open(pdf_file_path, "rb") as f:
                st.download_button("⬇️ Download PDF", f, file_name="summary.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"❌ Failed to export PDF summary.\n\n{e}")