from datetime import datetime

def filter_active_sensors(readings):
    return (r for r in readings if r.status == "active")

def extract_dates(readings):
    from datetime import date
    parse_date = date.fromisoformat
    return [parse_date(r.timestamp[:10]) for r in readings]

def moving_average(readings, window=200):
    temps = [r.temperature for r in readings]
    n = len(temps)
    if n < window:
        return []
        
    averages = [0.0] * (n - window + 1)
    current_sum = sum(temps[:window])
    inv_window = 1.0 / window
    averages[0] = current_sum * inv_window
    
    for i in range(window, n):
        current_sum += temps[i] - temps[i - window]
        averages[i - window + 1] = current_sum * inv_window
        
    return averages
