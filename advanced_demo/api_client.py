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
    from concurrent.futures import ThreadPoolExecutor
    
    # Materialize to a list in case sensor_ids is an iterator/generator, 
    # since we need to iterate over it twice (once for map, once for zip).
    sensor_ids_list = list(sensor_ids)
    
    with ThreadPoolExecutor() as executor:
        # Fetch locations concurrently to avoid N+1 I/O latency
        results = executor.map(fetch_sensor_location_sync, sensor_ids_list)
        return dict(zip(sensor_ids_list, results))
