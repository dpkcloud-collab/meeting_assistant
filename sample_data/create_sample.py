from gtts import gTTS
import os

# In order to create the mp3 for audio testing i am using gtts library(google text to speech)
meeting_text = """Rohan: Good morning everyone. Thanks for joining the weekly project sync meeting. Today we will review the progress of the Meeting Assistant project and discuss the next milestones. Deepak, since you are working on the backend architecture, could you start with a quick update?

Deepak: Sure, Rohan. Over the last few days I focused mainly on building the FastAPI backend and integrating the Whisper transcription pipeline. Right now the system can accept an audio file through an API endpoint, process it, and return the transcription successfully. I also started experimenting with the meeting analysis workflow that extracts tasks and summaries from the transcription.

Anita: That sounds good. Does the transcription handle longer meetings properly?

Deepak: Yes, I tested it with a few sample audio recordings. Whisper handled them quite well, though processing time increases slightly for longer files. I am planning to optimize it further by adding background processing so the API response doesn't block.

Rohan: That makes sense. For the next step we also need a clean architecture for the agent workflow. Have you started connecting the agents?

Deepak: Yes, I started implementing a graph-based workflow where the transcription result is passed to different nodes. One node will summarize the meeting, another will extract action items, and another might generate follow-up notes.

Anita: That will be very useful. From the product perspective we want the assistant to automatically identify who is responsible for tasks. That way users can quickly see action items without reading the full transcript.

Rohan: Exactly. Deepak, could you take ownership of the task extraction module?

Deepak: Yes, I can handle that.

Rohan: Great. Deepak, please implement the task extraction logic and integrate it into the backend pipeline by Wednesday, March 13th. The module should detect tasks, owners, and deadlines if they are mentioned in the meeting.

Deepak: Noted. I will complete the task extraction module by March 13th and share the API endpoint for testing.

Anita: Meanwhile, I will start working on the user interface. The idea is that users should be able to upload an audio file and see three sections: the transcription, the meeting summary, and the extracted tasks.

Rohan: That sounds good. Anita, could you create a basic UI prototype first?

Anita: Yes. I will design a simple interface using React where users can upload audio files and view the results returned by the API.

Rohan: Perfect. Anita, please finish the first UI prototype by Thursday, March 14th so that we can connect it with the backend.

Anita: Sure. I will have the upload screen and the results display ready by March 14th.

Deepak: Once the UI is ready, I can update the API responses to include structured JSON for summaries and tasks.

Rohan: Good idea. Also, we should ensure the response format is consistent so the frontend can easily parse it.

Anita: Yes, a structured JSON response would be ideal. Maybe something like transcription, summary, and tasks.

Deepak: That works. I will modify the API so that it returns a JSON object with three fields: transcription, summary, and action_items.

Rohan: Excellent. Now let's discuss testing. We should collect some realistic meeting recordings to test the assistant.

Anita: I can help with that. I will gather a few sample meeting recordings from our internal calls.

Rohan: That would be helpful. Anita, please upload at least five sample meeting recordings to the shared project folder by Monday, March 18th.

Anita: Sure, I will upload five recordings by March 18th.

Deepak: With those recordings I can test the system and evaluate how well the task extraction works.

Rohan: Great. Also Deepak, once the extraction module is ready, please write a short documentation explaining how the API works.

Deepak: Okay, I will write the backend API documentation by Friday, March 15th.

Anita: That will help me understand how to integrate the frontend properly.

Rohan: Another thing we should consider is generating meeting summaries automatically. That will be a key feature for users who just want the highlights.

Deepak: Yes, I was planning to add a summarization agent in the workflow.

Rohan: Good. Deepak, please add the summarization module to the agent workflow and have it ready by Monday, March 18th.

Deepak: Sure, I will implement the summarization module by March 18th.

Anita: Once that is ready, the UI can show a short summary at the top of the page.

Rohan: Exactly. The summary should ideally contain the key discussion points, decisions made, and action items.

Deepak: Understood. I will structure the summary so that it clearly highlights the important points.

Anita: That would improve readability for users.

Rohan: Alright, let's quickly recap the tasks so everyone is clear.

Rohan: Deepak, you will implement the task extraction module and integrate it into the backend by March 13th.

Rohan: Deepak, you will also write the backend API documentation by March 15th.

Rohan: Deepak, you will add the meeting summarization module by March 18th.

Deepak: Yes, I have noted all three tasks and the deadlines.

Rohan: Anita, you will create the frontend prototype by March 14th.

Rohan: Anita, you will also collect and upload five meeting recordings by March 18th for testing.

Anita: Yes, I will complete both tasks by the respective deadlines.

Rohan: Perfect. Once these tasks are done we can run an end-to-end test of the system.

Deepak: That will help us identify performance bottlenecks as well.

Anita: And we can also evaluate how accurate the task extraction is.

Rohan: Exactly. If everything works well, we can move towards building additional features like calendar integration and automated email summaries.

Deepak: That would be a great addition.

Anita: Yes, users would love automatic follow-up emails after meetings.

Rohan: Alright, I think we have covered everything for today. Thank you both for the updates and the discussion.

Deepak: Thanks everyone.

Anita: Thank you, see you in the next meeting.
"""

print("Generating audio file...")
tts = gTTS(text=meeting_text, lang='en')

# Save it as the filename your Whisper script expects
tts.save("sample_meeting.mp3")

print("Done! 'sample_meeting.mp3' is ready for testing.")