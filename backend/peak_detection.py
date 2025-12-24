import numpy as np
from scipy.ndimage import maximum_filter

def find_peaks(spectrogram_db, amp_min=-40):
    """
    Find local peaks in a spectrogram (in dB)
    """
    # Local maximum filter
    neighborhood = (20, 20)
    local_max = maximum_filter(spectrogram_db, size=neighborhood) == spectrogram_db

    # Apply amplitude threshold
    detected_peaks = np.logical_and(local_max, spectrogram_db >= amp_min)

    # Get peak coordinates
    peak_coords = np.argwhere(detected_peaks)

    return peak_coords

