def identify_instruments(audio_file):
    """
    Simulates a model that detects multiple segments for the same instrument.
    In a real app, this would use a sliding window over the Spectrogram.
    """
    # Logic: One instrument (e.g., 'Guitar') has multiple start/end entries.
    segments = [
        {"Instrument": "Drums", "Start": 0, "End": 60},
        {"Instrument": "Electric Guitar", "Start": 5, "End": 15},
        {"Instrument": "Electric Guitar", "Start": 40, "End": 55},  # Second appearance
        {"Instrument": "Piano", "Start": 10, "End": 30},
        {"Instrument": "Piano", "Start": 50, "End": 60},           # Second appearance
        {"Instrument": "Synthesizer", "Start": 25, "End": 45},
        {"Instrument": "Vocals", "Start": 12, "End": 58}
    ]
    return segments
