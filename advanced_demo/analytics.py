from datetime import datetime

def filter_active_sensors(readings):
    # Memory Bottleneck #2: Creates a massive new list in memory instead of yielding.
    for r in readings:
        if r.status == "active":
            yield r

def extract_dates(readings):
    # Runtime Bottleneck #1: datetime.strptime is very slow for bulk operations.
    # Since ISO8601 is fixed length, string slicing (r.timestamp[:10]) is vastly faster.
    return [datetime.fromisoformat(r.timestamp[:10]).date() for r in readings]

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
    
    for i in range(n - window):
        current_sum += temps[i + window] - temps[i]
        averages.append(current_sum / window)
        
    return averages
