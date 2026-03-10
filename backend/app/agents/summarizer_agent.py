import os
import json
from langchain_groq import ChatGroq
from backend.app.agents.utils.state import  MeetingState

def summarizer_node(state: MeetingState):
    print("\n--- AGENT: Summarizer is finalizing the report ---")
    # Initialize
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )
    # Get the existing insights from the Analyzer Agent (Detailed Analysis)
    analyzer_data = state.get('raw_insights', {})

    # Prepare context for the summary paragraph
    combined_context = f"""
    Transcript: {state.get('transcript')}
    Key Insights Found: {analyzer_data}
    """

    # Prompt to generate ONLY the summary paragraph
    prompt = f"""
    You are a professional Executive Assistant. 
    I will provide you with a meeting transcript and a list of extracted action items.

    YOUR ONLY TASK: Write a professional, high-level 2-sentence summary paragraph of the meeting. 

    CRITICAL RULES:
    - DO NOT list the specific action items, owners, or deadlines in this paragraph.
    - DO NOT mention specific dates like 'March 13th' in this paragraph.
    - Just describe the overall purpose and progress of the meeting.

    Return ONLY a JSON object:
    {{
      "summary_paragraph": "Your 2-sentence overview here"
    }}

    Data:
    {combined_context}
    """

    try:
        response = llm.invoke(prompt)
        content = response.content.replace("```json", "").replace("```", "").strip()
        summary_json = json.loads(content)

        # MERGE DATA MANUALLY
        final_analysis = {
            "analysis": {
                "summary": summary_json.get("summary_paragraph"),
                "action_items": analyzer_data.get("action_items", []),
                "key_decisions": analyzer_data.get("key_decisions", []),
                "sentiment": analyzer_data.get("sentiment", "Positive")
            }
        }

    except Exception as e:
        print(f"Error in Summarizer JSON parsing: {e}")
        # Fallback if AI fails to give JSON
        final_analysis = {
            "analysis": {
                "summary": "Meeting concluded with progress on backend and UI tasks.",
                "action_items": analyzer_data.get("action_items", []),
                "key_decisions": analyzer_data.get("key_decisions", []),
                "sentiment": "Positive"
            }
        }

    return {
        "final_summary": final_analysis,
        "status": "Completed"
    }