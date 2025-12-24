import librosa
import numpy as np

def load_audio(file_path, sample_rate=44100):
    """
    Load audio file and convert to mono with fixed sample rate
    """
    audio, sr = librosa.load(file_path, sr=sample_rate, mono=True)
    return audio, sr

def normalize_audio(audio):
    """
    Normalize audio to range [-1, 1]
    """
    max_val = np.max(np.abs(audio))
    if max_val == 0:
        return audio
    return audio / max_val

def preprocess_audio(file_path):
    audio, sr = load_audio(file_path)
    audio = normalize_audio(audio)
    return audio, sr

