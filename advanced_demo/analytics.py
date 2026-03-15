from datetime import datetime

def filter_active_sensors(readings):
    active_readings = []
    for r in readings:
        if r.status == "active":
            active_readings.append(r)
    return active_readings

from datetime import datetime, date

def extract_dates(readings):
    # Fast path: extract 'YYYY-MM-DD' and use the optimized fromisoformat
    iso_from = date.fromisoformat
    return [iso_from(r.timestamp[:10]) for r in readings]

def moving_average(readings, window=200):
    n = len(readings)
    if n < window or window <= 0:
        return []

    temps = [r.temperature for r in readings]
    num_results = n - window + 1
    averages = [0.0] * num_results
    
    current_sum = sum(temps[:window])
    averages[0] = current_sum / window
    
    for i in range(1, num_results):
        current_sum += temps[i + window - 1] - temps[i - 1]
        averages[i] = current_sum / window
    
    return averages
