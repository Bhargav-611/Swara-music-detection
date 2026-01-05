from collections import defaultdict
from db.fingerprint_dao import FingerprintDAO

def match_fingerprints(clip_fingerprints):
    # 1️⃣ Extract only hashes from clip
    clip_hashes = [h for h, _ in clip_fingerprints]

    # 2️⃣ ONE database query
    db_matches = FingerprintDAO.query_hashes_bulk(clip_hashes)

    if not db_matches:
        return None

    # 3️⃣ Voting
    song_match_count = defaultdict(int)

    for hash_value, song_id, _ in db_matches:
        song_match_count[song_id] += 1

    # 4️⃣ Find best matching song
    best_song_id = max(song_match_count, key=song_match_count.get)
    best_score = song_match_count[best_song_id]

    return best_song_id, best_score, song_match_count
