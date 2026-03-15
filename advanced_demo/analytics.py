from datetime import datetime

def filter_active_sensors(readings):
    return [r for r in readings if r.status == "active"]

def extract_dates(readings):
    return [datetime.fromisoformat(r.timestamp.replace('Z', '+00:00')).date() for r in readings]

def moving_average(readings, window=200):
    temps = [r.temperature for r in readings]
    n = len(temps)
    if n < window:
        return []
    
    # Calculate the initial window sum
    # Note: if window is 0, this will raise ZeroDivisionError, matching original behavior
    current_sum = sum(temps[:window])
    averages = [current_sum / window]
    
    # Update sum by adding the next element and removing the first element of the previous window
    for i in range(n - window):
        current_sum += temps[i + window] - temps[i]
        averages.append(current_sum / window)
        
    return averages
