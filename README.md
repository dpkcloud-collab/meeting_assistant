# Agentic Meeting Assistant (POC)

## Project Objective
The Agentic Meeting Assistant is a high-performance, AI-driven solution designed to transform raw meeting audio into structured, actionable business intelligence.

In a corporate environment where meetings consume significant time, this tool solves the "post-meeting lag" by:

- Automated Transcription: Converting speech to text with 95%+ accuracy.

- Intelligent Analysis: Using specialized AI agents to extract tasks, owners, and deadlines.

- Executive Summarization: Generating high-level overviews for leadership.

- Hybrid Processing: Providing flexibility between high-speed Cloud processing (Groq) and data-private Local processing (Whisper On-Prem).

---

## Technical Stack

- Backend: FastAPI (Python 3.10+)
- Agent Orchestration: LangGraph (Stateful, Multi-Agent Workflows)
- Transcription Engines: * Cloud: Groq LPU (Whisper-v3-turbo) - Latency: 2-5 seconds
- Local: OpenAI Whisper (Base Model) - Latency: Depends on Hardware
- LLM (Brain): Groq Llama 3.3-70B (High Intelligence) & 3.1-8B (Instant Analysis)
- Frontend: Streamlit (Python-based Rapid Prototyping)
- Environment: Virtualenv, Dotenv
---
## The Multi-Agent Workflow

The system operates as a sequential Agentic Graph. Each agent has a distinct "System Persona" to ensure high-quality, specialized output.

The Workflow Pipeline:

- Transcriber Node: Handles the heavy lifting of audio-to-text conversion.
- Analyzer Agent: Parses the raw text to extract structured JSON data (tasks, decisions).
- Summarizer Agent: Polishes the final report for executive readability.

---

## ADR: Mermaid Sequence & Flow

System Flow (Logic Graph)

````mermaid

graph TD
    A[Upload Audio] --> B{Transcriber Mode}
    B -- Groq Cloud --> C[Groq distil-whisper-v3]
    B -- Local On-Prem --> D[Whisper Base Model]
    C --> E[State: Transcript]
    D --> E
    E --> F[Analyzer Agent]
    F --> G[State: Action Items & Decisions]
    G --> H[Summarizer Agent]
    H --> I[Final Executive Report]
    I --> J[Streamlit UI Display]

````

## Sequence Diagram

````mermaid
sequenceDiagram
    participant User as User (Streamlit)
    participant API as FastAPI Backend
    participant Graph as LangGraph Orchestrator
    participant Groq as Groq Cloud / Local GPU

    User->>API: Upload MP3 & Select Mode
    API->>Graph: Initialize State
    Graph->>Groq: Request Transcription
    Groq-->>Graph: Return Text
    Graph->>Groq: Analyze Tasks & Summary
    Groq-->>Graph: Return Structured JSON
    Graph-->>API: Final State Object
    API-->>User: Display Structured Analysis

````

---

## Local Setup Instructions

### Prerequisites
- Python 3.10 or higher installed.
- FFmpeg installed and added to your System PATH (required for audio processing).
- A Groq API Key (get it at console.groq.com)

### Clone and Install


````bash
# Clone the repository
git clone <your-repo-url>
cd meeting_assistant

# Create virtual environment
python -m venv .venv
source .venv/bin/Scripts/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

## Dependency 
FFmpeg (Added to System PATH)
````


### Environment Configuration
Create a .env file in the backend/ directory:

````bash
GROQ_API_KEY=your_groq_api_key_here

````

### Running the Project
You need to run two separate terminals:

Terminal 1: FastAPI Backend

````bash
cd backend/app
python main.py

````
Terminal 2: Streamlit Frontend

````bash
streamlit run streamlit_app/app.py
````

For Sample data refer the attached mp3 file at below path

````bash
cp sample_data\sample_meeting.mp3
````

---

## Business Value (POC Results)
- Latency Reduction: By implementing the Groq whisper turbo, transcription time for a 3MB file was reduced from ~30 seconds (local CPU) to < 3 seconds.
- Cost Efficiency: Using open-source models (Llama 3) via Groq provides GPT-4 level intelligence at a fraction of the cost.
- Scalability: The LangGraph architecture allows for adding "Search Agents" or "Calendar Agents" in the future without breaking existing code.


---

## Future Roadmap & Enhancements
Phase 2 will focus on turning insights into direct actions.

###  Enterprise Integrations
Google/Outlook Calendar: Automatically book the "Next Steps" identified by the Analyzer Agent.

Slack/Jira: Push extracted Action Items directly to team project boards.

###  Real-time Diarization
Implement speaker identification to attribute specific decisions to specific stakeholders (e.g., "John Doe agreed to X").

###  Data Privacy & Security
PII Masking: Anonymize sensitive data (names, budgets) before cloud processing.

Local-First Mode: Optimization for fully air-gapped on-premise environments.

###  Sentiment & Trend Analysis
Analyze meeting sentiment over time to detect project risks or team morale shifts.