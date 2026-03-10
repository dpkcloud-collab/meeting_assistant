import sys
from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Agentic Meeting Assistant")

# Add this block:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with your UI URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
ENV_PATH = os.path.join(BASE_DIR, ".env")

print("ENV PATH:", ENV_PATH)
print("File exists:", os.path.exists(ENV_PATH))

load_dotenv(ENV_PATH, override=True)

print("Loaded GROQ KEY:", os.getenv("GROQ_API_KEY"))
# STEP 2: Path setup
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from fastapi import FastAPI
import uvicorn

# STEP 3: Import routes
from api.routes import router as meeting_router

app = FastAPI(title="Agentic Meeting Assistant")

# STEP 4: FFmpeg setup (read from .env)
ffmpeg_path = os.getenv("FFMPEG_PATH")
if ffmpeg_path:
    os.environ["PATH"] += os.pathsep + ffmpeg_path

app.include_router(meeting_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)