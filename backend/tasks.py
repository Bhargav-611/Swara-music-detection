import os
from fastapi import HTTPException
from utils.youtube_downloader import download_youtube_audio
from main_pipeline import main_pipeline


def process_youtube_task(youtube_url, temp_dir):
    """
    Background task:
    - Download YouTube audio
    - Generate fingerprints
    - Store in DB
    - Delete temp audio
    """

    audio_path = None

    try:
        audio_path, title = download_youtube_audio(
            youtube_url,
            temp_dir
        )

        main_pipeline(
            audio_path=audio_path,
            youtube_url=youtube_url,
            title=title
        )

    finally:
        # Always cleanup temp file
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)