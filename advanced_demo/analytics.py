from datetime import datetime

def filter_active_sensors(readings):
    # Memory Bottleneck #2: Creates a massive new list in memory instead of yielding.
    active_readings = []
    for r in readings:
        if r.status == "active":
            active_readings.append(r)
    return active_readings

def extract_dates(readings):
    # Runtime Bottleneck #1: datetime.strptime is very slow for bulk operations.
    # Since ISO8601 is fixed length, string slicing (r.timestamp[:10]) is vastly faster.
    dates = []
    for r in readings:
        dt = datetime.strptime(r.timestamp, "%Y-%m-%dT%H:%M:%SZ")
        dates.append(dt.date())
    return dates

def moving_average(readings, window=200):
    # Runtime/Algorithmic Bottleneck #2: Re-summing the entire window every iteration O(N*K).
    # Should use a running sum or collections.deque.
    temps = [r.temperature for r in readings]
    averages = []
    for i in range(len(temps) - window + 1):
        # sum() creates an internal loop calculating K elements every time
        avg = sum(temps[i:i+window]) / window
        averages.append(avg)
    return averages
