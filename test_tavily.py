import os
try:
    from dotenv import load_dotenv
except ImportError as e:
    print("Import Error: dotenv -", str(e))
    load_dotenv = lambda: False
try:
    from tavily import TavilyClient
except ImportError as e:
    print("Import Error: tavily -", str(e))
    TavilyClient = None

try:
    dotenv_success = load_dotenv()
    print("Dotenv Load Success:", dotenv_success)
    api_key = os.getenv("TAVILY_API_KEY")
    print("TAVILY_API_KEY:", api_key)
    if not api_key:
        print("Error: TAVILY_API_KEY is not set.")
    else:
        try:
            tavily = TavilyClient(api_key=api_key) if TavilyClient else None
            if tavily:
                response = tavily.search(query="test query", max_results=1)
                print("Search Response:", response)
            else:
                print("Error: TavilyClient not initialized due to import error.")
        except Exception as e:
            print("Tavily Error:", str(e))
except Exception as e:
    print("General Error:", str(e))