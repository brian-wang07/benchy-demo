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
            
        # Map header names to indices for performance and parity
        idx = {name: i for i, name in enumerate(header)}
        ts_i, sid_i, temp_i, stat_i = idx['timestamp'], idx['sensor_id'], idx['temperature'], idx['status']
        
        # Localize constructor for slight performance gain in loop
        constructor = SensorReading
        return [
            constructor(row[ts_i], row[sid_i], row[temp_i], row[stat_i])
            for row in reader
        ]
