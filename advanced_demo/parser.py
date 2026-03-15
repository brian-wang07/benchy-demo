import csv

class SensorReading:
    def __init__(self, timestamp, sensor_id, temperature, status):
        self.timestamp = timestamp
        self.sensor_id = sensor_id
        self.temperature = float(temperature)
        self.status = status

def parse_data(filename: str):
    readings = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            reading = SensorReading(
                row['timestamp'],
                row['sensor_id'],
                row['temperature'],
                row['status']
            )
            readings.append(reading)
    return readings
