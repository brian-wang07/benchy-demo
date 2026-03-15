import time
import tracemalloc
import os
from data_generator import generate_csv
from parser import parse_data
from analytics import filter_active_sensors, extract_dates, moving_average
from api_client import get_locations_for_sensors

tracemalloc.start()

def measure_performance(func, *args, **kwargs):
    print(f"\nRunning {func.__name__}...")
    # Reset peak memory trace before running the function
    tracemalloc.reset_peak()
    start_time = time.perf_counter()
    
    result = func(*args, **kwargs)
    
    end_time = time.perf_counter()
    _, peak_mem = tracemalloc.get_traced_memory()
    
    print(f"Time elapsed: {end_time - start_time:.4f} seconds")
    print(f"Peak memory: {peak_mem / 10**6:.2f} MB")
    return result

from concurrent.futures import ThreadPoolExecutor
from api_client import fetch_sensor_location_sync

def get_locations_for_sensors_parallel(sensor_ids, max_workers=20):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(fetch_sensor_location_sync, sensor_ids))

def main():
    csv_file = "sensor_data.csv"
    if not os.path.exists(csv_file):
        generate_csv(csv_file, 500000)
        
    readings = measure_performance(parse_data, csv_file)
    print(f"Parsed {len(readings)} readings.")
    
    active = measure_performance(filter_active_sensors, readings)
    print(f"Filtered {len(active)} active readings.")
    
    dates = measure_performance(extract_dates, active[:50000]) 
    print(f"Extracted dates for {len(dates)} readings.")
    
    averages = measure_performance(moving_average, active[:50000], window=200)
    
    unique_sensors = list({r.sensor_id for r in active[:5000]})
    # Optimized: replaced sequential call with a parallel execution wrapper
    locations = measure_performance(get_locations_for_sensors_parallel, unique_sensors[:200])
    print(f"Fetched locations for {len(locations)} sensors.")
    print(f"Calculated {len(averages)} moving averages.")

if __name__ == "__main__":
    main()
