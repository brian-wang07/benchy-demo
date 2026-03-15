from datetime import datetime

def filter_active_sensors(readings):
    active_readings = []
    for r in readings:
        if r.status == "active":
            active_readings.append(r)
    return active_readings

def extract_dates(readings):
    dates = []
    for r in readings:
        dt = datetime.strptime(r.timestamp, "%Y-%m-%dT%H:%M:%SZ")
        dates.append(dt.date())
    return dates

def moving_average(readings, window=200):
    temps = [r.temperature for r in readings]
    averages = []
    for i in range(len(temps) - window + 1):
        avg = sum(temps[i:i+window]) / window
        averages.append(avg)
    return averages
