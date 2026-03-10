import os
import io
from groq import Groq


def transcribe_audio(file_content: bytes, filename: str):
    """
    Accepts raw bytes to skip Disk I/O.
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Wrap bytes in a file-like object in memory
    audio_file = (filename, file_content)

    transcription = client.audio.transcriptions.create(
        file=audio_file,
        model="distil-whisper-large-v3-en",
        response_format="text",
        language="en"
    )
    return transcription