from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import traceback

from utils.youtube_downloader import download_youtube_audio
from main import process_song_with_youtube

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
    artist: str | None = "Unknown"


# -----------------------------
# API Endpoint
# -----------------------------
@app.post("/upload-youtube")
def upload_youtube_song(data: YouTubeRequest):
    audio_path = None

    try:
        # 1️⃣ Download YouTube audio temporarily
        audio_path, title = download_youtube_audio(
            data.youtube_url,
            TEMP_DIR
        )

        if not os.path.exists(audio_path):
            raise HTTPException(
                status_code=500,
                detail="Audio download failed"
            )

        # 2️⃣ Process song (fingerprint + DB store)
        success, message = process_song_with_youtube(
            audio_path=audio_path,
            youtube_url=data.youtube_url,
            artist=data.artist
        )

        # 3️⃣ Remove temp audio file
        try:
            os.remove(audio_path)
        except Exception:
            pass  # safe cleanup

        if not success:
            raise HTTPException(
                status_code=400,
                detail=message
            )

        return {
            "status": "success",
            "song_title": title,
            "youtube_url": data.youtube_url,
            "message": message
        }

    except HTTPException:
        raise

    except Exception as e:
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)

        print(traceback.format_exc())

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
