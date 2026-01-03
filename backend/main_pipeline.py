from main import process_song
from db.fingerprint_dao import FingerprintDAO

def main_pipeline(audio_path, youtube_url, title):

    fingerprints = process_song(
        audio_path,
        conditon=True
    )

    if not fingerprints:
        return False, "Song processing failed"

    # 5️⃣ Store in Database
    song_id = FingerprintDAO.insert_song(
        title=title,
        audio_url=youtube_url
    )

    print("Type of fingerprints:", type(fingerprints))
    print("Sample fingerprints:", fingerprints[:5] if isinstance(fingerprints, list) else fingerprints)


    FingerprintDAO.insert_fingerprints(song_id, fingerprints)

    return True, "Song processed and stored successfully"