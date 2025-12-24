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

peaks = find_peaks(spec_db)

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

plt.scatter(times_sec, freqs_hz, s=1, c="cyan", label="Peaks")
plt.title("Spectrogram with Peak Constellation")
plt.tight_layout()
plt.show()
