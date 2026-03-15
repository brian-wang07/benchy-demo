from datetime import datetime

def filter_active_sensors(readings):
    return [r for r in readings if r.status == "active"]

def extract_dates(readings):
    return [datetime.fromisoformat(r.timestamp[:10]).date() for r in readings]

def moving_average(readings, window=200):
    temps = [r.temperature for r in readings]
    n = len(temps)
    if n < window:
        return []
        
    averages = []
    current_sum = sum(temps[:window])
    averages.append(current_sum / window)
    
    for i in range(window, n):
        current_sum += temps[i] - temps[i - window]
        averages.append(current_sum / window)
        
    return averages
