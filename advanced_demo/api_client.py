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
    Optimized: Parallelizes I/O calls using ThreadPoolExecutor and deduplicates inputs.
    Reduces execution time from O(N) to O(1) concurrent latency.
    """
    if not sensor_ids:
        return {}

    # Deduplicate while preserving order to avoid redundant network calls
    unique_ids = []
    seen = set()
    for sid in sensor_ids:
        if sid not in seen:
            unique_ids.append(sid)
            seen.add(sid)

    # Use a ThreadPoolExecutor to perform the simulated I/O in parallel.
    # The default number of workers is typically sufficient for this scale.
    with ThreadPoolExecutor() as executor:
        # map executes the function concurrently across threads and preserves order
        results = list(executor.map(fetch_sensor_location_sync, unique_ids))

    return dict(zip(unique_ids, results))
