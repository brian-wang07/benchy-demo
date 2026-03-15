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
    Optimized: Parallelizes I/O-bound network calls using ThreadPoolExecutor.
    Reduces execution time from O(N * latency) to approx O(latency).
    """
    # Convert to list to handle generator inputs and allow multiple iterations (map + zip)
    ids = list(sensor_ids)
    if not ids:
        return {}

    with ThreadPoolExecutor() as executor:
        # Map submits all tasks and returns results in the original order.
        # This parallelizes the 10ms sleep in fetch_sensor_location_sync.
        results = executor.map(fetch_sensor_location_sync, ids)
        
        # zip and dict handle duplicate sensor_ids correctly, 
        # matching the original sequential loop's behavior.
        return dict(zip(ids, results))
