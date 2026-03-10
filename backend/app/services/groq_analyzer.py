import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get API key
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Initialize Groq client
client = Groq(api_key=groq_api_key)

def analyze_meeting(transcript):

    system_prompt = (
        "You are an expert Executive Assistant. Your task is to analyze meeting transcripts "
        "and extract structured insights. You MUST return the output in valid JSON format only."
    )
    user_prompt = f"""
    Please analyze the following meeting transcript:
    ---
    {transcript}
    ---

    Extract the following fields into a JSON object:

    1. "summary": A 2-3 sentence overview
    2. "action_items": List of tasks with owner and deadline if mentioned
    3. "key_decisions": Important decisions taken
    4. "sentiment": Overall tone of the meeting
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt} ],
        response_format={"type": "json_object"}
    )

    result = completion.choices[0].message.content

    return json.loads(result)