import time

def fetch_sensor_location_sync(sensor_id):
    """
    Simulates a network latency bottleneck (e.g., an HTTP GET to a remote API).
    Each call takes 10ms to simulate network transit time.
    """
    time.sleep(0.01) 
    return f"Location_Zone_{sensor_id.split('_')[-1]}"

from concurrent.futures import ThreadPoolExecutor

# Persistent cache to store results of previous API calls
_LOCATION_CACHE = {}

def get_locations_for_sensors(sensor_ids):
    """
    Optimized: Parallel execution and caching to resolve I/O bottleneck.
    Uses ThreadPoolExecutor to handle multiple simulated network calls concurrently.
    """
    # 1. Filter out IDs already in cache and deduplicate the rest
    unique_requested = set(sensor_ids)
    missing_ids = [sid for sid in unique_requested if sid not in _LOCATION_CACHE]
    
    # 2. Fetch missing sensor locations in parallel
    if missing_ids:
        # max_workers defaults to min(32, os.cpu_count() + 4), which is ideal for I/O
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(fetch_sensor_location_sync, missing_ids))
            # Update cache with new results
            for sid, location in zip(missing_ids, results):
                _LOCATION_CACHE[sid] = location
                
    # 3. Return a dictionary mapping every requested ID to its location from cache
    return {sid: _LOCATION_CACHE[sid] for sid in sensor_ids}
