from datetime import datetime

def filter_active_sensors(readings):
    return (r for r in readings if r.status == "active")

from datetime import date

def extract_dates(readings):
    return [date.fromisoformat(r.timestamp[:10]) for r in readings]

def moving_average(readings, window=200):
    n = len(readings)
    if n < window:
        return []
        
    temps = [r.temperature for r in readings]
    averages = [0.0] * (n - window + 1)
    
    current_sum = sum(temps[:window])
    averages[0] = current_sum / window
    
    for i in range(window, n):
        current_sum += temps[i] - temps[i - window]
        averages[i - window + 1] = current_sum / window
        
    return averages
