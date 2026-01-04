import os
from fastapi import FastAPI, HTTPException, UploadFile, File

from pydantic import BaseModel
from tasks import process_youtube_task

app = FastAPI(
    title="Shazam-like Audio Fingerprinting API",
    description="Upload YouTube link, generate fingerprints, store metadata",
    version="1.0"
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_DIR = "temp_audio"


class YouTubeRequest(BaseModel):
    youtube_url: str


@app.post("/upload-youtube")
def upload_youtube_song(data: YouTubeRequest):
    """
    Blocks until fingerprints are generated and stored
    """


    try:
        from db.fingerprint_dao import FingerprintDAO
        existing_song = FingerprintDAO.get_song_by_url(data.youtube_url)
        
        if existing_song:
             return {
                "status": "success",
                "message": "Song already exists in database",
                "song_id": existing_song["id"]
            }

        process_youtube_task(
            data.youtube_url,
            TEMP_DIR
        )

        return {
            "status": "success",
            "message": "Fingerprint generated and stored successfully"
        }


    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )



@app.post("/recognize-song")
def recognize_song_api(audio_file: UploadFile = File(...)):
    """
    Uploads an audio file and attempts to recognize the song.
    """
    file_location = f"{TEMP_DIR}/{audio_file.filename}"
    
    # Ensure temp directory exists
    import os
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
        
    try:
        with open(file_location, "wb") as buffer:
            import shutil
            shutil.copyfileobj(audio_file.file, buffer)
            
        # Convert to wav if needed
        if not file_location.lower().endswith(".wav"):
            print(f"Converting {file_location} to wav...")
            wav_location = os.path.splitext(file_location)[0] + ".wav"
            import subprocess
            try:
                subprocess.run(
                    ["ffmpeg", "-i", file_location, "-y", wav_location], 
                    check=True, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE
                )
                # Cleanup original file
                os.remove(file_location)
                file_location = wav_location
                print(f"Converted to {file_location}")
            except subprocess.CalledProcessError as e:
                print(f"FFmpeg conversion failed: {e}")
                raise HTTPException(status_code=500, detail="Audio conversion failed")
            
        from Detection.recognition_service import recognize_song
        success, result = recognize_song(file_location)
        
        if success:
            return {
                "status": "success",
                "result": result
            }
        else:
            return {
                "status": "error",
                "message": result
            }
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error processing audio: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup
        if os.path.exists(file_location):
            os.remove(file_location)

@app.get("/")
def health_check():
    return {"status": "ok"}