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
    from operator import itemgetter
    from itertools import starmap
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return []
            
        getter = itemgetter(
            header.index('timestamp'),
            header.index('sensor_id'),
            header.index('temperature'),
            header.index('status')
        )
        
        return list(starmap(SensorReading, map(getter, reader)))
