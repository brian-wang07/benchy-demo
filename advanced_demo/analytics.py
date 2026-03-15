from datetime import datetime

def filter_active_sensors(readings):
    active_readings = []
    for r in readings:
        if r.status == "active":
            active_readings.append(r)
    return active_readings

from datetime import date

def extract_dates(readings):
    dates = []
    # Cache the date constructor to avoid global lookups
    date_obj = date
    for r in readings:
        ts = r.timestamp
        # Format: %Y-%m-%dT%H:%M:%SZ (e.g., 2023-10-27T...)
        # Direct slicing is much faster than strptime
        d = date_obj(int(ts[:4]), int(ts[5:7]), int(ts[8:10]))
        dates.append(d)
    return dates

def moving_average(readings, window=200):
    n = len(readings)
    if n < window:
        return []

    temps = [r.temperature for r in readings]
    averages = []
    
    # Calculate the initial window sum
    current_window_sum = sum(temps[:window])
    averages.append(current_window_sum / window)
    
    # Slide the window across the rest of the list
    # complexity: O(N)
    for i in range(1, n - window + 1):
        # Subtract the element exiting the window and add the element entering it
        current_window_sum = current_window_sum - temps[i - 1] + temps[i + window - 1]
        averages.append(current_window_sum / window)
        
    return averages
