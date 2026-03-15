from datetime import datetime

def filter_active_sensors(readings):
    return [r for r in readings if r.status == "active"]

from datetime import datetime, date

def extract_dates(readings):
    # Runtime Bottleneck #1: datetime.strptime is very slow for bulk operations.
    # date.fromisoformat is significantly faster for fixed ISO8601 strings.
    return [date.fromisoformat(r.timestamp[:10]) for r in readings]

def moving_average(readings, window=200):
    # Runtime/Algorithmic Bottleneck #2: Re-summing the entire window every iteration O(N*K).
    # Optimized to O(N) using a sliding window sum.
    temps = [r.temperature for r in readings]
    n = len(temps)
    if n < window:
        return []
    
    current_sum = sum(temps[:window])
    averages = [current_sum / window]
    
    for i in range(n - window):
        current_sum += temps[i + window] - temps[i]
        averages.append(current_sum / window)
    return averages
