from dotenv import load_dotenv
import os

load_dotenv()
import whisper
from .utils.state import MeetingState

# def transcriber_node(state:MeetingState):
#     print("--- AGENT: Transcriber is processing audio ---")
#     model = whisper.load_model("base")
#     result = model.transcribe(state["audio_path"], fp16=False)
#     return {"transcript": result["text"], "status": "Transcribed"}


from groq import Groq

#
# def transcriber_node(state:MeetingState):
#     """
#     Accepts raw bytes to skip Disk I/O.
#     """
#     mode = state.get("transcription_mode", "local").lower()
#
#     client = Groq(api_key=os.getenv("GROQ_API_KEY"))
#     file_content = state["audio_path"]
#     filename="meetings.mp3"
#
#     # Wrap bytes in a file-like object in memory
#     audio_file = (filename, file_content)
#
#     transcription = client.audio.transcriptions.create(
#         file=audio_file,
#         model="whisper-large-v3-turbo",
#         response_format="text",
#         language="en"
#     )
#     return transcription
#


import os
from groq import Groq
import whisper


def transcriber_node(state: MeetingState):
    mode = state.get("transcription_mode", "local").lower()
    audio_path = state["audio_path"]

    # --- OPTION A: Groq Cloud (Ultra Fast) ---
    if mode == "groq":
        print("--- AGENT: Transcriber using GROQ CLOUD (distil-whisper) ---")
        try:
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            with open(audio_path, "rb") as file:
                transcription = client.audio.transcriptions.create(
                    file=(os.path.basename(audio_path), file.read()),
                    model="whisper-large-v3-turbo",
                    response_format="text",
                    language="en"
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