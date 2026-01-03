"""
End-to-end pipeline to:
1. Load and preprocess audio
2. Generate spectrogram
3. Detect spectral peaks
4. Generate audio fingerprints
5. (Optional) Store fingerprints in database
6. Test fingerprint lookup
"""

import os
import librosa.display
import matplotlib.pyplot as plt

from utils.audio_utils import preprocess_audio
from spectrogram import generate_spectrogram, magnitude_to_db
from peak_detection import find_peaks
from fingerprint import generate_fingerprints


SAMPLE_RATE = 44100
N_FFT = 4096
HOP_LENGTH = 2048
AMP_MIN_DB = -40

FAN_VALUE = 10
MIN_TIME_DELTA = 0.1
MAX_TIME_DELTA = 3.0

def process_song(audio_path, conditon=False):

    # 1️⃣ Audio Preprocessing
    audio, sr = preprocess_audio(audio_path)


    # 2️⃣ Spectrogram Generation
    spectrogram = generate_spectrogram(
    audio,
    sr,
    n_fft=N_FFT,
    hop_length=HOP_LENGTH
    )

    spectrogram_db = magnitude_to_db(spectrogram)


    # 3️⃣ Peak Detection
    peaks = find_peaks(spectrogram_db, amp_min=-40)

    print("Number of peaks detected:", len(peaks))

    if conditon and len(peaks) < 500:
        return False, "Too few peaks detected"


    # 4️⃣ Convert Peak Indices → Real Units
    times_sec = peaks[:, 1] * HOP_LENGTH / sr
    freqs_hz = peaks[:, 0] * sr / N_FFT

    peaks_converted = list(zip(times_sec, freqs_hz))

    
    # 5️⃣ Fingerprint Generation (Anchor–Target Hashing)
    fingerprints = generate_fingerprints(
        peaks_converted,
        fan_value=FAN_VALUE,
        min_time_delta=MIN_TIME_DELTA,
        max_time_delta=MAX_TIME_DELTA
    )
    print("Total fingerprints generated:", len(fingerprints))
    print("Sample fingerprints:", fingerprints[:5])

    if conditon and len(fingerprints) < 1000:
        return False, "Insufficient fingerprints"

    return fingerprints

    

    # plt.figure(figsize=(10, 4))
    # librosa.display.specshow(
    #     spectrogram_db ,
    #     sr=sr,
    #     hop_length=HOP_LENGTH,
    #     x_axis="time",
    #     y_axis="hz"
    # )

    # show peaks

    # plt.scatter(times_sec, freqs_hz, s=1, c="cyan", label="Peaks")
    # plt.title("Spectrogram with Peak Constellation")
    # plt.tight_layout()
    # plt.show()    