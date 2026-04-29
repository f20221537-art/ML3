def get_quick_data():
    return [
        {"Instrument": "Guitar", "Start": 0, "End": 30},
        {"Instrument": "Drums", "Start": 9, "End": 30},
        {"Instrument": "Voice", "Start": 18, "End": 30}
    ]

def get_realtime_frame(current_second):
    active = []
    if 0 <= current_second <= 30:
        active.append("Guitar")
    if 9 <= current_second <= 30:
        active.append("Drums")
    if 18 <= current_second <= 30:
        active.append("Voice")
    return active
