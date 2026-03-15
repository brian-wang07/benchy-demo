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
    
    def fetch_locations_concurrently(sensors):
        import concurrent.futures
        # Maximize concurrency by using a thread per sensor (ideal for completely IO-bound wait times)
        max_workers = len(sensors) if sensors else 1
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Process sensors concurrently by passing chunks of 1 to the API function
            results = executor.map(lambda s: get_locations_for_sensors([s]), sensors)
            return [loc for res in results for loc in res]

    locations = measure_performance(fetch_locations_concurrently, unique_sensors[:200])
    print(f"Fetched locations for {len(locations)} sensors.")
    print(f"Calculated {len(averages)} moving averages.")

if __name__ == "__main__":
    main()
