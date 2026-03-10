from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
import traceback

# --- CLEAN IMPORTS (Relative to 'app' root) ---
from backend.app.services.whisper_transcriber import transcribe_audio
from backend.app.services.groq_analyzer import  analyze_meeting
from backend.app.agents.graph import create_meeting_graph

router = APIRouter()

# --- PATH SETUP ---
# Ensures the 'uploads' folder is created in the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize the Agentic Graph (LangGraph)
agentic_app = create_meeting_graph()

# --- EXISTING LINEAR ENDPOINT ---
@router.post("/process")
async def process_meeting(file: UploadFile = File(...)):
    temp_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        transcript = transcribe_audio(temp_path)
        insights = analyze_meeting(transcript)
        return {
            "status": "success",
            "type": "linear_processing",
            "data": {
                "transcript": transcript,
                "analysis": insights
            }
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


# --- NEW AGENTIC ENDPOINT (FIXED REPETITION) ---
@router.post("/agentic-process")
async def process_meeting_agentic(file: UploadFile = File(...), mode: str = "groq", diarization: bool = False):
    """
    Triggers the LangGraph workflow and returns a clean, non-repetitive JSON.
    """
    temp_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        print("\n--- Starting Agentic Workflow ---")

        # Initial State for LangGraph

        initial_state = {
            "audio_path": temp_path,
            "transcription_mode": mode,
            "status": "Initiated",
            "transcript": None,
            "raw_insights": None,
            "final_summary": None,
            "enable_diarization": diarization,
        }

      

        final_state = agentic_app.invoke(initial_state)

        # --- DATA EXTRACTION ---
        analysis_block = final_state.get("final_summary", {}).get("analysis", {})

        return {
            "status": "success",
            "type": "agentic_workflow",
            "agent_journey": "Completed",
            "data": {
                "transcript": final_state.get("transcript"),
                "mode_used": mode,
                "analysis": analysis_block
            }
        }

    except Exception as e:
        print("\nAgentic Workflow Error")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Agent Error: {str(e)}")

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


