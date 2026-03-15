import time

def fetch_sensor_location_sync(sensor_id):
    """
    Simulates a network latency bottleneck (e.g., an HTTP GET to a remote API).
    Each call takes 10ms to simulate network transit time.
    """
    time.sleep(0.01) 
    return f"Location_Zone_{sensor_id.split('_')[-1]}"

from concurrent.futures import ThreadPoolExecutor

def get_locations_for_sensors(sensor_ids):
    """
    Optimized: Uses a ThreadPoolExecutor to handle I/O calls concurrently
    and deduplicates IDs to minimize total network requests.
    """
    if not sensor_ids:
        return {}

    # Deduplicate while preserving order to minimize redundant I/O calls
    unique_ids = list(dict.fromkeys(sensor_ids))
    
    # Use ThreadPoolExecutor to parallelize the simulated 10ms network latency.
    # max_workers is capped at 100 to balance concurrency vs thread overhead.
    with ThreadPoolExecutor(max_workers=min(len(unique_ids), 100)) as executor:
        # map ensures results are returned in the order of unique_ids
        results = list(executor.map(fetch_sensor_location_sync, unique_ids))
    
    # Create a mapping for quick O(1) lookups
    lookup = dict(zip(unique_ids, results))
    
    # Reconstruct the dictionary for all requested IDs (including duplicates)
    # This ensures exact functional parity with the original sequential implementation.
    return {sid: lookup[sid] for sid in sensor_ids}
