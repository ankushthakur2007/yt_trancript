from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend calls (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for dev, restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "FastAPI running!"}

@app.get("/transcript/{video_id}")
def get_transcript(video_id: str):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry['text'] for entry in transcript])
        return {"transcript": full_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
