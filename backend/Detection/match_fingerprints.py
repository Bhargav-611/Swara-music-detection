from backend.db.fingerprint_dao import FingerprintDAO
from collections import defaultdict

def match_fingerprints(clip_fingerprints):
    song_match_count = defaultdict(int)

    for hash_value, _ in clip_fingerprints:
        matches = FingerprintDAO.query_hash(hash_value)

        for song_id, _ in matches:
            song_match_count[song_id] += 1

    if not song_match_count:
        return None

    # 3️⃣ Find best matching song
    best_song_id = max(song_match_count, key=song_match_count.get)
    best_score = song_match_count[best_song_id]

    return best_song_id, best_score, song_match_count