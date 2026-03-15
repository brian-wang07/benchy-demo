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

from concurrent.futures import ThreadPoolExecutor

def main():
    csv_file = "sensor_data.csv"
    if not os.path.exists(csv_file):
        generate_csv(csv_file, 500000)
        
    readings = measure_performance(parse_data, csv_file)
    print(f"Parsed {len(readings)} readings.")
    
    active = measure_performance(filter_active_sensors, readings)
    print(f"Filtered {len(active)} active readings.")
    
    # Optimization: Slice once and reuse for both extract_dates and moving_average
    active_subset = active[:50000]
    dates = measure_performance(extract_dates, active_subset)
    print(f"Extracted dates for {len(dates)} readings.")
    
    averages = measure_performance(moving_average, active_subset, window=200)
    
    # Run API test on a small unique subset
    unique_sensors = list({r.sensor_id for r in active[:5000]})
    sensor_ids_to_fetch = unique_sensors[:200]

    def get_locations_parallel(sensor_ids):
        """
        Wraps the sequential API client to perform requests in parallel chunks.
        Maintains functional parity by flattening results back into the original format.
        """
        chunk_size = 20
        chunks = [sensor_ids[i:i + chunk_size] for i in range(0, len(sensor_ids), chunk_size)]
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            batch_results = list(executor.map(get_locations_for_sensors, chunks))
        
        if not batch_results:
            return []
        
        # Flatten results based on return type (list or dict)
        if isinstance(batch_results[0], dict):
            merged = {}
            for b in batch_results: merged.update(b)
            return merged
        return [item for sublist in batch_results for item in sublist]

    locations = measure_performance(get_locations_parallel, sensor_ids_to_fetch)
    print(f"Fetched locations for {len(locations)} sensors.")
    print(f"Calculated {len(averages)} moving averages.")

if __name__ == "__main__":
    main()
