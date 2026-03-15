import csv
import random
from datetime import datetime, timedelta

def generate_csv(filename: str, num_rows: int = 500000):
    start_time = datetime(2026, 1, 1)
    statuses = ["active", "inactive", "error"]
    # Pre-generate sensor IDs to avoid f-string overhead in the loop
    sensor_ids = [f"sensor_{i}" for i in range(1, 1001)]
    
    def data_generator():
        curr_dt = start_time
        delta = timedelta(minutes=1)
        # Local variable caching for faster access
        _choice = random.choice
        _uniform = random.uniform
        _round = round
        
        for _ in range(num_rows):
            # isoformat() is significantly faster than strftime()
            # Adding 'Z' suffix matches the original ISO8601 requirement
            yield (
                curr_dt.isoformat() + "Z",
                _choice(sensor_ids),
                _round(_uniform(-20.0, 50.0), 2),
                _choice(statuses)
            )
            curr_dt += delta

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "sensor_id", "temperature", "status"])
        # writerows with a generator reduces the number of Python->C transitions
        writer.writerows(data_generator())

if __name__ == "__main__":
    print("Generating 500k rows of sensor data...")
    generate_csv("sensor_data.csv")
    print("Data generation complete.")
