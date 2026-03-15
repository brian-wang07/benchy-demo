import csv

class SensorReading:
    __slots__ = ('timestamp', 'sensor_id', 'temperature', 'status')
    def __init__(self, timestamp, sensor_id, temperature, status):
        self.timestamp = timestamp
        self.sensor_id = sensor_id
        self.temperature = float(temperature)
        self.status = status

def parse_data(filename: str):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            return []
        
        # Pre-calculate indices to maintain robustness against column order changes
        # while keeping the inner loop extremely fast.
        t_idx = header.index('timestamp')
        s_idx = header.index('sensor_id')
        temp_idx = header.index('temperature')
        st_idx = header.index('status')
        
        cls = SensorReading
        # List comprehension is significantly faster than manual loop with .append()
        return [cls(r[t_idx], r[s_idx], r[temp_idx], r[st_idx]) for r in reader]
