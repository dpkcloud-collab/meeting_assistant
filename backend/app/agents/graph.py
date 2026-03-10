from langgraph.graph import StateGraph, END
from backend.app.agents.utils.state import MeetingState
from backend.app.agents.summarizer_agent import summarizer_node
from backend.app.agents.transcriber_agent import transcriber_node
from backend.app.agents.analyzer_agent import analyzer_node


def create_meeting_graph():
    workflow = StateGraph(MeetingState)

    # Add the specialized agents
    workflow.add_node("transcriber", transcriber_node)
    workflow.add_node("analyzer", analyzer_node)
    workflow.add_node("summarizer", summarizer_node)

    # Define the communication sequence
    workflow.set_entry_point("transcriber")
    workflow.add_edge("transcriber", "analyzer")
    workflow.add_edge("analyzer", "summarizer")
    workflow.add_edge("summarizer", END)

    return workflow.compile()