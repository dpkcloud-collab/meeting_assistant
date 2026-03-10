from dotenv import load_dotenv
import os

load_dotenv()
import whisper
from .utils.state import MeetingState



from groq import Groq



import os
from groq import Groq
import whisper


def transcriber_node(state: MeetingState):
    mode = state.get("transcription_mode", "local").lower()
    audio_path = state["audio_path"]

    # Check if diarization is enabled in the state
    enable_diarization = state.get("enable_diarization", False)

    # --- OPTION A: Groq Cloud (Ultra Fast) ---
    if mode == "groq":
        print("--- AGENT: Transcriber using GROQ CLOUD (distil-whisper) ---")
        try:
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            # Use specific prompting to simulate diarization for the POC
            diarization_prompt = (
                "Identify different speakers in this meeting and label them clearly "
                "as 'Speaker A:', 'Speaker B:', etc., based on voice changes."
            ) if enable_diarization else ""

            with open(audio_path, "rb") as file:
                transcription = client.audio.transcriptions.create(
                    file=(os.path.basename(audio_path), file.read()),
                    model="whisper-large-v3-turbo",
                    response_format="text",
                    language="en",
                    prompt=diarization_prompt,
                )
            return {"transcript": transcription, "status": "Transcribed (Groq)"}
        except Exception as e:
            print(f"Groq failed, falling back to local: {e}")
            mode = "local"  # Fallback if API fails

    # --- OPTION B: Local Whisper (Existing Implementation) ---
    if mode == "local":
        print("--- AGENT: Transcriber using LOCAL WHISPER (Base Model) ---")
        # Existing Implementation
        model = whisper.load_model("base")
        # fp16=False is necessary for CPU/certain laptop GPUs
        result = model.transcribe(audio_path, fp16=False)
        return {"transcript": result["text"], "status": "Transcribed (Local)"}