from collections import defaultdict
from backend.db.fingerprint_dao import FingerprintDAO
from backend.utils.audio_utils import preprocess_audio
from backend.spectrogram import generate_spectrogram, magnitude_to_db
from backend.peak_detection import find_peaks
from backend.fingerprint import generate_fingerprints
import os


def recognize_song(audio_path):
    # 1️⃣ Generate fingerprints from clip
    audio, sr = preprocess_audio(audio_path)

    spec = generate_spectrogram(audio, sr)
    spec_db = magnitude_to_db(spec)

    peaks = find_peaks(spec_db, amp_min=-40)

    hop_length = 2048
    n_fft = 4096

    times_sec = peaks[:, 1] * hop_length / sr
    freqs_hz = peaks[:, 0] * sr / n_fft
    peaks_converted = list(zip(times_sec, freqs_hz))

    clip_fingerprints = generate_fingerprints(
        peaks_converted,
        fan_value=10,
        min_time_delta=0.1,
        max_time_delta=3.0
    )

    print("Clip fingerprints:", len(clip_fingerprints))

    # 2️⃣ Match fingerprints with DB
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


# ---------- TEST ----------
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    clip_path = os.path.join(
        BASE_DIR, "..", "..", "data", "songs", "kalank_clip.wav"
    )

    result = recognize_song(clip_path)

    if result:
        song_id, score, all_scores = result
        print("\nMatch counts:", dict(all_scores))
        print("\n✅ Identified song_id:", song_id)
        print("✅ Match score:", score)
    else:
        print("❌ No match found")
    