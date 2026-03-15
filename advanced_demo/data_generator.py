import csv
import random
from datetime import datetime, timedelta

def generate_csv(filename: str, num_rows: int = 500000):
    start_time = datetime(2026, 1, 1)
    statuses = ("active", "inactive", "error")
    sensors = tuple(f"sensor_{i}" for i in range(1, 1001))
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "sensor_id", "temperature", "status"])
        
        choice = random.choice
        uniform = random.uniform
        delta = timedelta(minutes=1)
        
        def row_generator():
            dt = start_time
            for _ in range(num_rows):
                yield [
                    dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    choice(sensors),
                    round(uniform(-20.0, 50.0), 2),
                    choice(statuses)
                ]
                dt += delta
                
        writer.writerows(row_generator())

if __name__ == "__main__":
    print("Generating 500k rows of sensor data...")
    generate_csv("sensor_data.csv")
    print("Data generation complete.")
