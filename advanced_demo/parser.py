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
        try:
            header = next(reader)
        except StopIteration:
            return []
        
        idx = {name: i for i, name in enumerate(header)}
        t_idx = idx['timestamp']
        s_idx = idx['sensor_id']
        temp_idx = idx['temperature']
        stat_idx = idx['status']
        
        cls = SensorReading
        return [cls(row[t_idx], row[s_idx], row[temp_idx], row[stat_idx]) for row in reader]
