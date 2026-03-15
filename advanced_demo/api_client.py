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
    Optimized: Uses a thread pool to perform I/O-bound API calls in parallel.
    Includes deduplication to prevent redundant network requests.
    """
    if not sensor_ids:
        return {}

    # Deduplicate sensor IDs to avoid redundant API calls
    unique_sensor_ids = list(set(sensor_ids))
    
    # Use ThreadPoolExecutor to handle I/O bound tasks in parallel.
    # The default number of workers is sufficient for most I/O scenarios.
    with ThreadPoolExecutor() as executor:
        # map() handles the distribution of tasks and preserves the order of results
        results = executor.map(fetch_sensor_location_sync, unique_sensor_ids)
    
    # Create the mapping from the unique results
    return dict(zip(unique_sensor_ids, results))
