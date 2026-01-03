from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

from tasks import process_youtube_task

app = FastAPI(
    title="Shazam-like Audio Fingerprinting API",
    description="Upload YouTube link, generate fingerprints, store metadata",
    version="1.0"
)

TEMP_DIR = "temp_audio"


# -----------------------------
# Request Model
# -----------------------------
class YouTubeRequest(BaseModel):
    youtube_url: str


# -----------------------------
# API Endpoint
# -----------------------------
@app.post("/upload-youtube")
def upload_youtube_song(
    data: YouTubeRequest,
    background_tasks: BackgroundTasks
):
    """
    Accepts a YouTube URL and starts audio
    fingerprinting in the background.
    """

    background_tasks.add_task(
        process_youtube_task,
        data.youtube_url,
        TEMP_DIR
    )

    # Immediate response (non-blocking)
    return {
        "status": "accepted",
        "message": "Song processing started in background"
    }
