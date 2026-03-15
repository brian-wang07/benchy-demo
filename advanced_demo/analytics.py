from datetime import datetime

def filter_active_sensors(readings):
    # Memory Bottleneck #2: Creates a massive new list in memory instead of yielding.
    for r in readings:
        if r.status == "active":
            yield r

def extract_dates(readings):
    # Runtime Bottleneck #1: datetime.strptime is very slow for bulk operations.
    # Since ISO8601 is fixed length, string slicing (r.timestamp[:10]) is vastly faster.
    from datetime import date
    return [date(int(r.timestamp[:4]), int(r.timestamp[5:7]), int(r.timestamp[8:10])) for r in readings]

def moving_average(readings, window=200):
    # Runtime/Algorithmic Bottleneck #2: Re-summing the entire window every iteration O(N*K).
    # Should use a running sum or collections.deque.
    temps = [r.temperature for r in readings]
    n = len(temps)
    if n < window:
        return []

    averages = []
    current_sum = sum(temps[:window])
    averages.append(current_sum / window)

    for i in range(1, n - window + 1):
        current_sum += temps[i + window - 1] - temps[i - 1]
        averages.append(current_sum / window)

    return averages
