from datetime import datetime

def filter_active_sensors(readings):
    active_readings = []
    for r in readings:
        if r.status == "active":
            active_readings.append(r)
    return active_readings

def extract_dates(readings):
    from datetime import date
    dates = []
    cache = {}
    # Cache the date object constructor for the specific fixed format
    # Format: "YYYY-MM-DDTHH:MM:SSZ"
    for r in readings:
        ts = r.timestamp
        # Slice the date portion "YYYY-MM-DD"
        date_str = ts[:10]
        if date_str in cache:
            dates.append(cache[date_str])
        else:
            # Faster than strptime: manual slice and date constructor
            d_obj = date(int(date_str[:4]), int(date_str[5:7]), int(date_str[8:10]))
            cache[date_str] = d_obj
            dates.append(d_obj)
    return dates

def moving_average(readings, window=200):
    n = len(readings)
    if n < window:
        return []

    # Extract temperatures once to avoid repeated attribute lookups
    temps = [r.temperature for r in readings]
    
    # Pre-allocate result list for speed
    averages = [0.0] * (n - window + 1)
    
    # Initialize the first window sum
    current_sum = sum(temps[:window])
    averages[0] = current_sum / window
    
    # Slide the window
    for i in range(1, n - window + 1):
        # Subtract element leaving (i-1), add element entering (i + window - 1)
        current_sum += temps[i + window - 1] - temps[i - 1]
        averages[i] = current_sum / window
        
    return averages
