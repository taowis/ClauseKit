from langdetect import detect, DetectorFactory

# Fix seed for consistent results
DetectorFactory.seed = 42

def detect_language(text):
    """
    Detects the language of the input text and normalizes the code.

    Returns:
        str: 'en' for English, 'zh' for Chinese, or other language code
    """
    try:
        lang = detect(text)
        if lang.startswith("zh"):
            return "zh"
        if lang.startswith("en"):
            return "en"
        return lang
    except:
        return "unknown"