import csv
import random
from datetime import datetime, timedelta

def generate_csv(filename: str, num_rows: int = 500000):
    start_time = datetime(2026, 1, 1)
    statuses = ["active", "inactive", "error"]
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "sensor_id", "temperature", "status"])
        for i in range(num_rows):
            dt = start_time + timedelta(minutes=i)
            # Fixed ISO8601 format
            ts = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
            sensor_id = f"sensor_{random.randint(1, 1000)}"
            temp = round(random.uniform(-20.0, 50.0), 2)
            status = random.choice(statuses)
            writer.writerow([ts, sensor_id, temp, status])

if __name__ == "__main__":
    print("Generating 500k rows of sensor data...")
    generate_csv("sensor_data.csv")
    print("Data generation complete.")
