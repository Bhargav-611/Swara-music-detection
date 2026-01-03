from main import process_song
from db.fingerprint_dao import FingerprintDAO

def main_pipeline(audio_path, youtube_url, artist="Unknown"):

    fingerprints, song_name = process_song(
        audio_path,
        conditon=True
    )

    if not fingerprints:
        return False, "Song processing failed"

    # 5️⃣ Store in Database
    song_id = FingerprintDAO.insert_song(
        title=song_name,
        artist=artist,
        audio_url=youtube_url
    )

    FingerprintDAO.insert_fingerprints(
        song_id,
        fingerprints
    )

    return True, "Song processed and stored successfully"