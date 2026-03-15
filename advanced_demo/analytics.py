from datetime import datetime

def filter_active_sensors(readings):
    # Memory Bottleneck #2: Creates a massive new list in memory instead of yielding.
    active_readings = []
    for r in readings:
        if r.status == "active":
            active_readings.append(r)
    return active_readings

def extract_dates(readings):
    return [datetime.fromisoformat(r.timestamp[:10]).date() for r in readings]

def moving_average(readings, window=200):
    temps = [r.temperature for r in readings]
    averages = []
    n = len(temps)
    if n < window:
        return averages
        
    current_sum = sum(temps[:window])
    averages.append(current_sum / window)
    
    for i in range(1, n - window + 1):
        current_sum += temps[i + window - 1] - temps[i - 1]
        averages.append(current_sum / window)
        
    return averages
