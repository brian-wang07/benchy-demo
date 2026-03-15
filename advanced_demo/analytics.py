from datetime import datetime

def filter_active_sensors(readings):
    active_readings = []
    for r in readings:
        if r.status == "active":
            active_readings.append(r)
    return active_readings

def extract_dates(readings):
    dates = []
    # Local variable lookups are faster in loops
    from_iso = datetime.fromisoformat
    date_cache = {}
    
    for r in readings:
        # The date part is the first 10 characters 'YYYY-MM-DD'
        # Slicing is significantly faster than parsing the full string
        day_str = r.timestamp[:10]
        
        # Cache results to avoid redundant date object creation for the same day
        if day_str in date_cache:
            dates.append(date_cache[day_str])
        else:
            d = from_iso(day_str).date()
            date_cache[day_str] = d
            dates.append(d)
    return dates

def moving_average(readings, window=200):
    if not readings:
        return []
    temps = [r.temperature for r in readings]
    n = len(temps)
    if n < window:
        return []
    
    # Pre-allocate the results list for better performance
    res_len = n - window + 1
    averages = [0.0] * res_len
    
    # Initial window sum
    current_sum = sum(temps[:window])
    averages[0] = current_sum / window
    
    # Slide the window: O(1) update per iteration instead of O(W)
    for i in range(1, res_len):
        current_sum += temps[i + window - 1] - temps[i - 1]
        averages[i] = current_sum / window
    return averages
