import time
import tracemalloc
import os
from data_generator import generate_csv
from parser import parse_data
from analytics import filter_active_sensors, extract_dates, moving_average
from api_client import get_locations_for_sensors

def measure_performance(func, *args, **kwargs):
    print(f"\nRunning {func.__name__}...")
    tracemalloc.start()
    start_time = time.perf_counter()
    
    result = func(*args, **kwargs)
    
    end_time = time.perf_counter()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(f"Time elapsed: {end_time - start_time:.4f} seconds")
    print(f"Peak memory: {peak_mem / 10**6:.2f} MB")
    return result

from collections import namedtuple
import csv

Reading = namedtuple('Reading', ['sensor_id', 'value', 'date', 'is_active'])

def parse_data_optimized(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        # Using namedtuple and list comprehension for memory and speed efficiency
        return [Reading(row[0], float(row[1]), row[2], row[3] == 'True') for row in reader]

def main():
    csv_file = "sensor_data.csv"
    if not os.path.exists(csv_file):
        generate_csv(csv_file, 500000)
        
    readings = measure_performance(parse_data_optimized, csv_file)
    print(f"Parsed {len(readings)} readings.")
    
    active = measure_performance(filter_active_sensors, readings)
    print(f"Filtered {len(active)} active readings.")
    
    dates = measure_performance(extract_dates, active[:50000]) # Run on subset to save time
    print(f"Extracted dates for {len(dates)} readings.")
    
    def moving_average_optimized(data, window):
        if not data or window <= 0 or window > len(data):
            return []
        vals = [r.value for r in data]
        n = len(vals)
        res = [0.0] * (n - window + 1)
        curr_sum = sum(vals[:window])
        res[0] = curr_sum / window
        for i in range(1, n - window + 1):
            curr_sum += vals[i + window - 1] - vals[i - 1]
            res[i] = curr_sum / window
        return res

    averages = measure_performance(moving_average_optimized, active[:50000], window=200)
    
    from concurrent.futures import ThreadPoolExecutor
    from api_client import fetch_sensor_location_sync
    
    unique_sensors = list({r.sensor_id for r in active[:5000]})
    
    def get_locations_concurrent(sensor_ids):
        with ThreadPoolExecutor(max_workers=20) as executor:
            return list(executor.map(fetch_sensor_location_sync, sensor_ids))

    locations = measure_performance(get_locations_concurrent, unique_sensors[:200])
    print(f"Fetched locations for {len(locations)} sensors.")
    print(f"Calculated {len(averages)} moving averages.")

if __name__ == "__main__":
    main()
