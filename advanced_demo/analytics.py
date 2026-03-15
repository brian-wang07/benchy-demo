from datetime import datetime

def filter_active_sensors(readings):
    # Memory Bottleneck #2: Creates a massive new list in memory instead of yielding.
    return [r for r in readings if r.status == "active"]

def extract_dates(readings):
    # Runtime Bottleneck #1: datetime.strptime is very slow for bulk operations.
    # Since ISO8601 is fixed length, string slicing (r.timestamp[:10]) is vastly faster.
    return [datetime.fromisoformat(r.timestamp[:10]).date() for r in readings]

def moving_average(readings, window=200):
    # Runtime/Algorithmic Bottleneck #2: Re-summing the entire window every iteration O(N*K).
    # Should use a running sum or collections.deque.
    n = len(readings)
    if n < window:
        return []
        
    temps = [r.temperature for r in readings]
    current_sum = sum(temps[:window])
    averages = [current_sum / window]
    
    for i in range(window, n):
        current_sum += temps[i] - temps[i - window]
        averages.append(current_sum / window)
        
    return averages
