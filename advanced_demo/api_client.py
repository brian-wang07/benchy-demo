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
    locations = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(fetch_sensor_location_sync, sensor_ids)
        for sid, loc in zip(sensor_ids, results):
            locations[sid] = loc
            
    return locations
