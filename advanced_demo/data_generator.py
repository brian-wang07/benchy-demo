import csv
import random
from datetime import datetime, timedelta

def generate_csv(filename: str, num_rows: int = 500000):
    start_time = datetime(2026, 1, 1)
    statuses = ["active", "inactive", "error"]
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "sensor_id", "temperature", "status"])
        
        dt = start_time
        delta = timedelta(minutes=1)
        sensor_ids = [f"sensor_{i}" for i in range(1, 1001)]
        
        # Localize functions for faster lookup in hot loop
        writer_writerow = writer.writerow
        choice = random.choice
        uniform = random.uniform
        
        for _ in range(num_rows):
            # Fixed ISO8601 format
            ts = dt.isoformat(timespec='seconds') + "Z"
            sensor_id = choice(sensor_ids)
            temp = round(uniform(-20.0, 50.0), 2)
            status = choice(statuses)
            writer_writerow([ts, sensor_id, temp, status])
            dt += delta

if __name__ == "__main__":
    print("Generating 500k rows of sensor data...")
    generate_csv("sensor_data.csv")
    print("Data generation complete.")
