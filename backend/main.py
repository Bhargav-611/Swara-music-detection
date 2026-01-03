from utils.audio_utils import preprocess_audio
import librosa.display
from spectrogram import generate_spectrogram, magnitude_to_db
from peak_detection import find_peaks
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

audio_path = os.path.join(
    BASE_DIR, "..", "data", "songs", "adhiveshan.wav"
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


from fingerprint import generate_fingerprints

fingerprints = generate_fingerprints(peaks_converted, 
                                    fan_value=10,
                                    min_time_delta=0.1,
                                    max_time_delta=3.0)

print("Total fingerprints generated:", len(fingerprints))
print("Sample fingerprints:", fingerprints[:5])