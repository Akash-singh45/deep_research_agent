import os
try:
    from dotenv import load_dotenv
except ImportError as e:
    print("Import Error: dotenv -", str(e))
    load_dotenv = lambda: False
try:
    from graph.langgraph_flow import build_graph
except ImportError as e:
    print("Import Error: graph.langgraph_flow -", str(e))
    build_graph = lambda: None

# Debug environment and imports
print("Python Version:", os.popen("python --version").read())
print("Working Directory:", os.getcwd())
dotenv_success = load_dotenv()
print("Dotenv Load Success:", dotenv_success)
print("Dotenv File Path:", os.path.abspath(".env"))
print("TAVILY_API_KEY:", os.getenv("TAVILY_API_KEY"))
print("GEMINI_API_KEY:", os.getenv("GOOGLE_API_KEY"))

def main(query: str):
    try:
        if not build_graph:
            raise ValueError("build_graph not available due to import error.")
        # Initialize the LangGraph workflow
        graph = build_graph()
        
        # Define initial state
        initial_state = {
            "query": query,
            "research_data": [],
            "drafted_answer": ""
        }
        
        # Run the graph
        final_state = graph.invoke(initial_state)
        
        # Output the final answer
        print("\nFinal Answer:")
        print(final_state["drafted_answer"])
    except Exception as e:
        print("Error in main:", str(e))

# if __name__ == "__main__":
#     # Example query
#     sample_query =  "What are the latest advancements in artificial intelligence in 2025?"
#     main(sample_query)

if __name__ == "__main__":
    queries = [
        "What are recent developments in renewable energy?",
        "What is the status of quantum computing in 2025?",
        "What are advancements in biotechnology in 2025?"
    ]
    for query in queries:
        print(f"\nRunning query: {query}")
        main(query)