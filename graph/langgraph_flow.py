from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
import operator
from agents.research_agent import research_web
from agents.drafting_agent import draft_answer

# Define the state
class ResearchState(TypedDict):
    query: str
    research_data: list
    drafted_answer: str

# Define the nodes
def research_node(state: ResearchState) -> ResearchState:
    """Node for performing research."""
    research_data = research_web.invoke({"query": state["query"]})
    return {"research_data": research_data}

def drafting_node(state: ResearchState) -> ResearchState:
    """Node for drafting the answer."""
    drafted_answer = draft_answer.invoke({
        "query": state["query"],
        "research_data": state["research_data"]
    })
    return {"drafted_answer": drafted_answer}

# Build the graph
def build_graph():
    workflow = StateGraph(ResearchState)
    
    # Add nodes
    workflow.add_node("research", research_node)
    workflow.add_node("drafting", drafting_node)
    
    # Define edges
    workflow.set_entry_point("research")
    workflow.add_edge("research", "drafting")
    workflow.add_edge("drafting", END)
    
    # Compile the graph
    return workflow.compile()