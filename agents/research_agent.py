import os
import json
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file
except ImportError as e:
    print("Import Error: dotenv -", str(e))
    load_dotenv = lambda: False
try:
    from tavily import TavilyClient
except ImportError as e:
    print("Import Error: tavily -", str(e))
    TavilyClient = None
try:
    from langchain_core.tools import tool
except ImportError as e:
    print("Import Error: langchain_core.tools -", str(e))
    tool = lambda x: x
try:
    from google.generativeai import GenerativeModel
    import google.generativeai as genai
except ImportError as e:
    print("Import Error: google.generativeai -", str(e))
    GenerativeModel = None
    genai = None
try:
    from utils.text_cleaner import clean_text
except ImportError as e:
    print("Import Error: utils.text_cleaner -", str(e))
    def clean_text(text): return text

# Configure Gemini API
try:
    if genai:
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = GenerativeModel("gemini-1.5-pro")
    else:
        model = None
except Exception as e:
    print("Gemini API Error:", str(e))
    model = None

# Initialize Tavily client with error handling
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY is not set in environment variables. Please check your .env file.")
try:
    tavily = TavilyClient(api_key=tavily_api_key) if TavilyClient else None
except Exception as e:
    print("Tavily Client Error:", str(e))
    tavily = None

# Caching functions
def load_cache():
    """Load cached search results from cache.json."""
    cache_file = "data/cache.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    """Save search results to cache.json."""
    with open("data/cache.json", "w") as f:
        json.dump(cache, f, indent=2)

@tool
def research_web(query: str) -> list:
    """Perform a web search using Tavily and summarize results with Gemini, with caching."""
    try:
        if not tavily or not model:
            return [{"error": "Tavily or Gemini not initialized properly."}]

        # Check cache first
        cache = load_cache()
        if query in cache:
            return cache[query]

        # Perform Tavily search if not in cache
        response = tavily.search(query=query, max_results=5)
        results = response.get("results", [])
        
        # Extract relevant content
        research_data = []
        for result in results:
            content = result.get("content", "")
            cleaned_content = clean_text(content)
            research_data.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": cleaned_content
            })
        
        # Summarize with Gemini
        summary_prompt = (
            f"Summarize the following research data into a concise paragraph (100-150 words):\n"
            f"{str(research_data)}\n"
            f"Focus on key insights relevant to the query: {query}"
        )
        response = model.generate_content(summary_prompt)
        summary = response.text if response.text else "No summary generated."
        
        research_data.append({"summary": clean_text(summary)})
        
        # Save to cache
        cache[query] = research_data
        save_cache(cache)
        
        return research_data
    except Exception as e:
        return [{"error": f"Research failed: {str(e)}"}]