import csv

class SensorReading:
    __slots__ = ('timestamp', 'sensor_id', 'temperature', 'status')
    def __init__(self, timestamp, sensor_id, temperature, status):
        self.timestamp = timestamp
        self.sensor_id = sensor_id
        self.temperature = float(temperature)
        self.status = status

def parse_data(filename: str):
    with open(filename, 'r', newline='') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return []
        
        # Map header names to indices to maintain parity with DictReader's name-based access
        # while benefiting from the speed of positional indexing.
        idx = {name: i for i, name in enumerate(header)}
        t_idx, s_idx, temp_idx, st_idx = idx['timestamp'], idx['sensor_id'], idx['temperature'], idx['status']
        
        # Use a list comprehension for efficient list construction
        return [
            SensorReading(row[t_idx], row[s_idx], row[temp_idx], row[st_idx])
            for row in reader
        ]
