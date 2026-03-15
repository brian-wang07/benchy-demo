import csv
import random
from datetime import datetime, timedelta

def generate_csv(filename: str, num_rows: int = 500000):
    start_time = datetime(2026, 1, 1)
    statuses = ["active", "inactive", "error"]
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "sensor_id", "temperature", "status"])
        
        sensor_ids = [f"sensor_{i}" for i in range(1, 1001)]
        dt = start_time
        delta = timedelta(minutes=1)
        uniform = random.uniform
        
        chunk_size = 10000
        rem = num_rows
        while rem > 0:
            current = min(chunk_size, rem)
            sensors = random.choices(sensor_ids, k=current)
            stats = random.choices(statuses, k=current)
            rows = []
            for i in range(current):
                ts = dt.isoformat(timespec='seconds') + "Z"
                temp = round(uniform(-20.0, 50.0), 2)
                rows.append([ts, sensors[i], temp, stats[i]])
                dt += delta
            writer.writerows(rows)
            rem -= current

if __name__ == "__main__":
    print("Generating 500k rows of sensor data...")
    generate_csv("sensor_data.csv")
    print("Data generation complete.")
