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

def main():
    csv_file = "sensor_data.csv"
    if not os.path.exists(csv_file):
        generate_csv(csv_file, 500000)
        
    readings = measure_performance(parse_data, csv_file)
    print(f"Parsed {len(readings)} readings.")
    
    active = measure_performance(filter_active_sensors, readings)
    # Clear reference to large original list to reduce peak memory footprint
    readings = None 
    print(f"Filtered {len(active)} active readings.")
    
    # Cache the subset to avoid repeated slicing/copying
    active_subset = active[:50000]
    
    dates = measure_performance(extract_dates, active_subset)
    print(f"Extracted dates for {len(dates)} readings.")
    
    averages = measure_performance(moving_average, active_subset, window=200)
    
    # Optimization: Find up to 200 unique IDs with early exit instead of processing all 5000
    unique_sensors = []
    seen = set()
    for r in active_subset[:5000]:
        sid = r.sensor_id
        if sid not in seen:
            seen.add(sid)
            unique_sensors.append(sid)
            if len(unique_sensors) == 200:
                break

    locations = measure_performance(get_locations_for_sensors, unique_sensors)
    print(f"Fetched locations for {len(locations)} sensors.")
    print(f"Calculated {len(averages)} moving averages.")

if __name__ == "__main__":
    main()
