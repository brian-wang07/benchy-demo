import time

def fetch_sensor_location_sync(sensor_id):
    """
    Simulates a network latency bottleneck (e.g., an HTTP GET to a remote API).
    Each call takes 10ms to simulate network transit time.
    """
    time.sleep(0.01) 
    return f"Location_Zone_{sensor_id.split('_')[-1]}"

import concurrent.futures

def get_locations_for_sensors(sensor_ids):
    """
    I/O Bottleneck: Synchronous N+1 API calls.
    Iterates sequentially, waiting for each network call to finish before starting the next.
    """
    if not sensor_ids:
        return {}
        
    # Use a ThreadPoolExecutor with higher concurrency for I/O bound tasks
    workers = min(100, len(sensor_ids))
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        # map preserves the order, and dict(zip()) processes it natively in C
        return dict(zip(sensor_ids, executor.map(fetch_sensor_location_sync, sensor_ids)))

