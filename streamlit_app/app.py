import streamlit as st
import requests
import os
import pandas as pd

# Page Config
st.set_page_config(page_title="Agentic Meeting Assistant", page_icon="🎙️", layout="wide")

if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None

st.title("🎙️ Agentic Meeting Assistant")
st.markdown("Upload your meeting audio to get AI-powered transcriptions, summaries, and action items.")

# Sidebar for Configuration
st.sidebar.header("Settings")
api_url = st.sidebar.text_input("API URL", "http://127.0.0.1:8000/api/v1/agentic-process")

# Diarization Toggle in Sidebar
enable_diarization = st.sidebar.checkbox("Enable Speaker Diarization", value=False, help="Identify different speakers (Speaker A, Speaker B)")


# File Uploader
uploaded_file = st.file_uploader("Choose a meeting recording (mp3, wav, m4a)", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')

    # Model Selection
    mode = st.radio(
        "Select Transcription Engine:",
        ["Groq (Cloud - 3s)", "Local (Private - 2m)"],
        index=0,
        horizontal=True
    )
    api_mode = "groq" if "Groq" in mode else "local"

    if st.button("🚀 Analyze Meeting"):
        with st.spinner("Processing through AI Agents... (Transcribing -> Analyzing -> Summarizing)"):
            try:
                # Prepare the file for the POST request
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                # Passing both mode and diarization flag to backend
                params = {"mode": api_mode, "diarization": str(enable_diarization).lower()}

                response = requests.post(f"{api_url}?mode={api_mode}", files=files)
                # Hit the FastAPI Endpoint
                # response = requests.post(api_url, files=files)

                if response.status_code == 200:
                    result = response.json().get("data", {})
                    analysis = result.get("analysis", {})

                    st.success("✅ Analysis Complete!")

                    # Combine all data into the format the PDF service expects
                    full_data_for_pdf = {
                        "transcript": result.get("transcript"),
                        "analysis": analysis
                    }
                    

                    # Add a download button using the st.download_button widget
                    try:
                        pdf_response = requests.post("http://127.0.0.1:8000/api/v1/download-pdf", json=full_data_for_pdf)
                        if pdf_response.status_code == 200:
                            print(f"DEBUG: Received PDF size: {len(response.content)} bytes")
                            st.session_state.pdf_bytes = pdf_response.content
                            print(f"DEBUG: Received PDF size 2nd: {len(st.session_state.pdf_bytes)} bytes")

                          
                    except Exception as e:
                        st.error("Could not generate PDF download.")

                    # Layout: 2 Columns for Summary and Decisions
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("📝 Executive Summary")
                        st.info(analysis.get("summary", "No summary available."))
                        st.metric("Sentiment", analysis.get("sentiment", "N/A"))

                    with col2:
                        st.subheader("🎯 Key Decisions")
                        decisions = analysis.get("key_decisions", [])
                        for d in decisions:
                            # Handle both string and dict formats
                            text = d.get("decision") if isinstance(d, dict) else d
                            st.write(f" {text}")

                    # Action Items Table
                    st.divider()
                    st.subheader("📋 Action Items")
                    action_items = analysis.get("action_items", [])
                    if action_items:
                        df = pd.DataFrame(action_items)
                        # Reorder columns for better look
                        df = df[['task', 'owner', 'deadline']]
                        st.table(df)
                    else:
                        st.write("No action items detected.")

                    # Full Transcript (Expandable)
                    st.divider()
                    with st.expander("📄 View Full Transcript"):
                        st.text_area("", result.get("transcript"), height=300)

                else:
                    st.error(f"Error: {response.status_code} - {response.text}")

                # 3. SHOW DOWNLOAD BUTTON ONLY IF BYTES EXIST
                if st.session_state.pdf_bytes:
                    st.download_button(
                        label="📥 Download Executive PDF Report",
                        data=st.session_state.pdf_bytes,
                        file_name="Meeting_Report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Connection Error: {str(e)}")

st.sidebar.markdown("---")


st.sidebar.info("This POC uses LangGraph + Groq Whisper + Groq Llama 3 for real-time meeting intelligence.")

