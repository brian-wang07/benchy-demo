import time

def fetch_sensor_location_sync(sensor_id):
    """
    Simulates a network latency bottleneck (e.g., an HTTP GET to a remote API).
    Each call takes 10ms to simulate network transit time.
    """
    time.sleep(0.01) 
    return f"Location_Zone_{sensor_id.split('_')[-1]}"

def get_locations_for_sensors(sensor_ids):
    """
    I/O Bottleneck: Synchronous N+1 API calls.
    Iterates sequentially, waiting for each network call to finish before starting the next.
    """
    import concurrent.futures
    
    # Deduplicate while preserving the original insertion order
    unique_sids = list(dict.fromkeys(sensor_ids))
    locations = {}
    
    if not unique_sids:
        return locations
        
    # Use ThreadPoolExecutor to perform the I/O calls concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(100, len(unique_sids))) as executor:
        # executor.map guarantees the results are returned in the exact order of unique_sids
        results = executor.map(fetch_sensor_location_sync, unique_sids)
        for sid, result in zip(unique_sids, results):
            locations[sid] = result
            
    return locations
