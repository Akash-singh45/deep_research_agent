import re

def clean_text(text: str) -> str:
    """Clean and format text by removing extra spaces, newlines, and special characters."""
    # Remove excessive whitespace and newlines
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove special characters (keep basic punctuation)
    text = re.sub(r'[^\w\s.,!?]', '', text)
    return text