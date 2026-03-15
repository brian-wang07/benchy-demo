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
    print(f"Filtered {len(active)} active readings.")
    
    dates = measure_performance(extract_dates, active[:50000]) # Run on subset to save time
    print(f"Extracted dates for {len(dates)} readings.")
    
    averages = measure_performance(moving_average, active[:50000], window=200)
    
    # Run API test on a small unique subset to avoid hanging the benchmark
    unique_sensors = list({r.sensor_id for r in active[:5000]})
    
    def parallel_get_locations(sensors):
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=50) as executor:
            # Pass chunks of 1 to run the underlying sync fetches concurrently
            results = list(executor.map(get_locations_for_sensors, [[s] for s in sensors]))
        
        if not results:
            return get_locations_for_sensors([])
            
        if isinstance(results[0], dict):
            merged = {}
            for r in results:
                merged.update(r)
            return merged
        elif isinstance(results[0], list):
            merged = []
            for r in results:
                merged.extend(r)
            return merged
        return results

    locations = measure_performance(parallel_get_locations, unique_sensors[:200])
    print(f"Fetched locations for {len(locations)} sensors.")
    print(f"Calculated {len(averages)} moving averages.")

if __name__ == "__main__":
    main()
