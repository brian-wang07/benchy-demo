import csv

class SensorReading:
    # Memory Bottleneck #1: Lacks __slots__. 
    # Python creates a __dict__ for every instance, leading to large memory overhead.
    __slots__ = ('timestamp', 'sensor_id', 'temperature', 'status')

    def __init__(self, timestamp, sensor_id, temperature, status):
        self.timestamp = timestamp
        self.sensor_id = sensor_id
        self.temperature = float(temperature)
        self.status = status

def parse_data(filename: str):
    readings = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return readings
            
        t_idx = header.index('timestamp')
        s_idx = header.index('sensor_id')
        temp_idx = header.index('temperature')
        stat_idx = header.index('status')
        
        for row in reader:
            if not row:
                continue
            reading = SensorReading(
                row[t_idx],
                row[s_idx],
                row[temp_idx],
                row[stat_idx]
            )
            readings.append(reading)
    return readings
