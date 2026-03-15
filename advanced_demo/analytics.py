from datetime import datetime

def filter_active_sensors(readings):
    # Memory Bottleneck #2: Creates a massive new list in memory instead of yielding.
    active_readings = []
    for r in readings:
        if r.status == "active":
            active_readings.append(r)
    return active_readings

def extract_dates(readings):
    return [datetime(int(r.timestamp[0:4]), int(r.timestamp[5:7]), int(r.timestamp[8:10])).date() for r in readings]

def moving_average(readings, window=200):
    temps = [r.temperature for r in readings]
    if len(temps) < window:
        return []
    
    current_sum = sum(temps[:window])
    averages = [current_sum / window]
    
    for i in range(1, len(temps) - window + 1):
        current_sum += temps[i + window - 1] - temps[i - 1]
        averages.append(current_sum / window)
        
    return averages
