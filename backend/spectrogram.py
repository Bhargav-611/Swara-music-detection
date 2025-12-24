import librosa
import numpy as np

def generate_spectrogram(audio, sr, n_fft=4096, hop_length=2048):
    """
    Generate magnitude spectrogram using STFT
    """
    stft = librosa.stft(
        audio,
        n_fft=n_fft,
        hop_length=hop_length,
        window="hann"
    )
    magnitude = np.abs(stft)
    return magnitude

def magnitude_to_db(magnitude):
    return librosa.amplitude_to_db(magnitude, ref=np.max)
