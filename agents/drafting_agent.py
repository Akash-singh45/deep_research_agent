from langchain_core.tools import tool
from google.generativeai import GenerativeModel
import google.generativeai as genai
import os
from utils.text_cleaner import clean_text

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = GenerativeModel("gemini-1.5-pro")

@tool
def draft_answer(query: str, research_data: list) -> str:
    """Generate a polished answer based on research data using Gemini."""
    try:
        # Prepare prompt for drafting
        prompt = (
            f"Based on the following research data, provide a clear and concise answer (200-300 words) to the query: {query}\n"
            f"Research Data:\n{str(research_data)}\n"
            f"Ensure the answer is well-structured, informative, and directly addresses the query."
        )
        
        # Generate answer with Gemini
        response = model.generate_content(prompt)
        answer = response.text if response.text else "No answer generated."
        
        return clean_text(answer)
    except Exception as e:
        return f"Drafting failed: {str(e)}"