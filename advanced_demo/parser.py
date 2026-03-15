import csv

class SensorReading:
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
            return

        # Pre-map column names to indices for fast O(1) lookup during iteration
        indices = {name: i for i, name in enumerate(header)}
        ts_idx = indices['timestamp']
        sid_idx = indices['sensor_id']
        temp_idx = indices['temperature']
        stat_idx = indices['status']

        for row in reader:
            yield SensorReading(
                row[ts_idx],
                row[sid_idx],
                row[temp_idx],
                row[stat_idx]
            )
