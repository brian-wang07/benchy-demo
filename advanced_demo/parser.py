import csv

class SensorReading:
    __slots__ = ['timestamp', 'sensor_id', 'temperature', 'status']

    def __init__(self, timestamp, sensor_id, temperature, status):
        self.timestamp = timestamp
        self.sensor_id = sensor_id
        self.temperature = float(temperature)
        self.status = status

def parse_data(filename: str):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield SensorReading(
                row['timestamp'],
                row['sensor_id'],
                row['temperature'],
                row['status']
            )
