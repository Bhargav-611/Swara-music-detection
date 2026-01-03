from collections import defaultdict
from backend.db.fingerprint_dao import FingerprintDAO
from backend.utils.audio_utils import preprocess_audio
from backend.spectrogram import generate_spectrogram, magnitude_to_db
from backend.peak_detection import find_peaks
from backend.fingerprint import generate_fingerprints
from main import process_song
from match_fingerprints import match_fingerprints
import os

def recognize_song():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    clip_path = os.path.join(
        BASE_DIR, "..", "temp_audio", "songs", "kalank_clip.wav"
    )

    fingerprints = process_song(clip_path)

    result = match_fingerprints(fingerprints)

    if result:
        song_id, score, all_scores = result
        print("\nMatch counts:", dict(all_scores))
        print("\n✅ Identified song_id:", song_id)
        print("✅ Match score:", score)
        return True, f"Identified song_id: {song_id} with score: {score}"
    else:
        print("❌ No match found")
        return False, "No match found"
    