from typing import TypedDict, List, Optional

class MeetingState(TypedDict):
    audio_path: str
    transcript: Optional[str]
    raw_insights: Optional[dict]
    final_summary: Optional[str]
    status: str
    transcription_mode: str  # "groq" or "local"