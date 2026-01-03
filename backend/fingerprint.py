import hashlib

def generate_fingerprints(peaks, fan_value=5,
                          min_time_delta=0.5,
                          max_time_delta=3.0):
    """
    Generate anchor-target fingerprints
    peaks: array of (time_sec, freq_hz)
    """
    fingerprints = []

    # Sort peaks by time
    peaks = sorted(peaks, key=lambda x: x[0])

    for i in range(len(peaks)):
        t1, f1 = peaks[i]

        for j in range(1, fan_value + 1):
            if i + j >= len(peaks):
                break

            t2, f2 = peaks[i + j]
            delta_t = t2 - t1

            if min_time_delta <= delta_t <= max_time_delta:
                # Create hash string
                hash_input = f"{int(f1)}|{int(f2)}|{round(delta_t, 2)}"
                hash_val = hashlib.sha1(hash_input.encode()).hexdigest()[:20]

                fingerprints.append((hash_val, float(t1)))

    return fingerprints
