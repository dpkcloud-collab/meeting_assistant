from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

from langchain_groq import ChatGroq
from .utils.state import MeetingState

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found. Check your .env file")

    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api_key
    )


def analyzer_node(state: MeetingState):
    print("--- AGENT: Analyzer is extracting insights ---")
    llm = get_llm()
    prompt = f"""
    Analyze the following meeting transcript and extract structured insights.

    Return ONLY valid JSON in the following format:

    {{
      "action_items": [
        {{
          "task": "",
          "owner": "",
          "deadline": ""
        }}
      ],
      "key_decisions": [
        {{
          "decision": "",
          "description": ""
        }}
      ],
      "sentiment": ""
    }}

    Transcript:
    {state['transcript']}
    """

    response = llm.invoke(prompt)

    raw_output = response.content

    # Extract JSON from markdown if the model wraps it in ```json blocks
    match = re.search(r"\{.*\}", raw_output, re.DOTALL)

    if match:
        try:
            parsed_json = json.loads(match.group())
        except json.JSONDecodeError:
            parsed_json = {
                "action_items": [],
                "key_decisions": [],
                "sentiment": "unknown",
                "error": "Invalid JSON returned by LLM"
            }
    else:
        parsed_json = {
            "action_items": [],
            "key_decisions": [],
            "sentiment": "unknown",
            "error": "Failed to parse JSON",
            "raw_output": raw_output
        }

    return {
        "raw_insights": parsed_json,
        "status": "Analyzed"
    }