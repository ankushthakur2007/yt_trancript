from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logger setup
logging.basicConfig(level=logging.INFO)

@app.get("/")
def root():
    return {"message": "API is running!"}

@app.get("/transcript/{video_id}")
def get_transcript(video_id: str):
    try:
        logging.info(f"Fetching transcript for video_id: {video_id}")
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry['text'] for entry in transcript])
        return {"transcript": full_text}
    
    except TranscriptsDisabled:
        logging.error("Transcripts are disabled for this video.")
        raise HTTPException(status_code=404, detail="Transcripts are disabled for this video.")
    
    except NoTranscriptFound:
        logging.error("No transcript found for this video.")
        raise HTTPException(status_code=404, detail="No transcript found for this video.")
    
    except VideoUnavailable:
        logging.error("Video is unavailable.")
        raise HTTPException(status_code=404, detail="Video is unavailable.")
    
    except Exception as e:
        logging.exception("Unexpected error occurred")
        raise HTTPException(status_code=500, detail=str(e))
