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
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            return
        
        try:
            ts_idx = header.index('timestamp')
            sid_idx = header.index('sensor_id')
            temp_idx = header.index('temperature')
            stat_idx = header.index('status')
        except ValueError:
            # Replicate DictReader KeyError behavior for missing headers
            for col in ('timestamp', 'sensor_id', 'temperature', 'status'):
                if col not in header:
                    raise KeyError(col)
        
        for row in reader:
            try:
                yield SensorReading(row[ts_idx], row[sid_idx], row[temp_idx], row[stat_idx])
            except IndexError:
                # Fallback for short rows, matching DictReader's behavior of returning None for missing columns
                row_dict = dict(zip(header, row))
                yield SensorReading(
                    row_dict.get('timestamp'),
                    row_dict.get('sensor_id'),
                    row_dict.get('temperature'),
                    row_dict.get('status')
                )
