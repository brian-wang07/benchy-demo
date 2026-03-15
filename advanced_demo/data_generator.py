import csv
import random
from datetime import datetime, timedelta

def generate_csv(filename: str, num_rows: int = 500000):
    start_time = datetime(2026, 1, 1)
    statuses = ["active", "inactive", "error"]
    sensor_ids = [f"sensor_{i}" for i in range(1, 1001)]
    choice = random.choice
    uniform = random.uniform
    delta = timedelta(minutes=1)
    dt = start_time
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "sensor_id", "temperature", "status"])
        
        chunk_size = 10000
        for chunk_start in range(0, num_rows, chunk_size):
            chunk_end = min(chunk_start + chunk_size, num_rows)
            chunk = []
            for _ in range(chunk_end - chunk_start):
                # Fixed ISO8601 format
                ts = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                sensor_id = choice(sensor_ids)
                temp = round(uniform(-20.0, 50.0), 2)
                status = choice(statuses)
                chunk.append([ts, sensor_id, temp, status])
                dt += delta
            writer.writerows(chunk)

if __name__ == "__main__":
    print("Generating 500k rows of sensor data...")
    generate_csv("sensor_data.csv")
    print("Data generation complete.")
