def get_quick_data():
    """Returns the full overlapping dataset at once."""
    return [
        {"Instrument": "Guitar", "Start": 0, "End": 30},
        {"Instrument": "Drums", "Start": 9, "End": 30},
        {"Instrument": "Voice", "Start": 18, "End": 30}
    ]

def get_realtime_frame(current_second):
    """
    Simulates the model output at a specific timestamp.
    Matches your test: 
    0-9: Guitar
    9-18: Guitar + Drums
    18-30: Guitar + Drums + Voice
    """
    active = []
    if 0 <= current_second <= 30:
        active.append("Guitar")
    if 9 <= current_second <= 30:
        active.append("Drums")
    if 18 <= current_second <= 30:
        active.append("Voice")
    return active
