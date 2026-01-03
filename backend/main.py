from utils.audio_utils import preprocess_audio
import librosa.display
from spectrogram import generate_spectrogram, magnitude_to_db
from peak_detection import find_peaks
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

audio_path = os.path.join(
    BASE_DIR, "..", "data", "songs", "song1.wav"
)

audio, sr = preprocess_audio(audio_path)

spec = generate_spectrogram(audio, sr)
spec_db = magnitude_to_db(spec)

peaks = find_peaks(spec_db, amp_min=-40)

print("Number of peaks detected:", len(peaks))

hop_length = 2048
n_fft = 4096

times_sec = peaks[:, 1] * hop_length / sr
freqs_hz = peaks[:, 0] * sr / n_fft

plt.figure(figsize=(10, 4))
librosa.display.specshow(
    spec_db,
    sr=sr,
    hop_length=hop_length,
    x_axis="time",
    y_axis="hz"
)

# show peaks

# plt.scatter(times_sec, freqs_hz, s=1, c="cyan", label="Peaks")
# plt.title("Spectrogram with Peak Constellation")
# plt.tight_layout()
# plt.show()

# Convert peaks to (time_sec, freq_hz)
peaks_converted = list(zip(times_sec, freqs_hz))


# generate_fingerprints (fan_value=10(5->low, 15->high), min_time_delta=0.1, max_time_delta=3.0)
from fingerprint import generate_fingerprints

fingerprints = generate_fingerprints(peaks_converted, 
                                    fan_value=10,
                                    min_time_delta=0.1,
                                    max_time_delta=3.0)

print("Total fingerprints generated:", len(fingerprints))
print("Sample fingerprints:", fingerprints[:5])


# store in db
from db.fingerprint_dao import FingerprintDAO

# remove comment to store in db

# 1. Insert song metadata
# song_id = FingerprintDAO.insert_song(
#     title="jay hoo",
#     artist="BAPS"
# )

# # 2. Insert fingerprints
# FingerprintDAO.insert_fingerprints(song_id, fingerprints)

# print("Fingerprints stored for song_id:", song_id)

print("Sample fingerprints:", fingerprints[:5])

test_hash = fingerprints[0][0]   # first hash

results = FingerprintDAO.query_hash(test_hash)

print("Query hash:", test_hash)
print("Results from DB:", results[:10])
