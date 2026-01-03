import matplotlib.pyplot as plt
import librosa.display
plt.scatter(times_sec, freqs_hz, s=1, c="cyan", label="Peaks")
plt.title("Spectrogram with Peak Constellation")
plt.tight_layout()
plt.show()