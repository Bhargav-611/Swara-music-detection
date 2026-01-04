import os

from db.fingerprint_dao import FingerprintDAO
from main import process_song
from Detection.match_fingerprints import match_fingerprints

def recognize_song(audio_file_path):
    if not os.path.exists(audio_file_path):
        return False, f"Audio file not found: {audio_file_path}"

    fingerprints = process_song(audio_file_path)

    result = match_fingerprints(fingerprints)

    MIN_MATCH_SCORE = 20

    if result:
        song_id, score, all_scores = result

        if score < MIN_MATCH_SCORE:
            print(f"❌ Match score {score} is below threshold {MIN_MATCH_SCORE}")
            return False, "No match found (score too low)"

        # Get song details from database
        song_details = FingerprintDAO.get_song_by_id(song_id)
        
        print("\nMatch counts:", dict(all_scores))
        print("\n✅ Identified song_id:", song_id)

        print("✅ Match score:", score)
        
        return True, {
            "song_id": song_id,
            "score": score,
            "match_counts": dict(all_scores),
            "song": song_details
        }
    else:
        print("❌ No match found")
        return False, "No match found"
    