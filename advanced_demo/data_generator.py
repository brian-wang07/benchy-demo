import csv
import random
from datetime import datetime, timedelta

def generate_csv(filename: str, num_rows: int = 500000):
    start_time = datetime(2026, 1, 1)
    statuses = ["active", "inactive", "error"]
    # Pre-cache sensor names to avoid 500,000 f-string evaluations
    sensor_ids = [f"sensor_{i}" for i in range(1, 1001)]
    delta = timedelta(minutes=1)
    
    # Local lookups for performance
    choice = random.choice
    uniform = random.uniform
    round_val = round

    def data_generator():
        curr_dt = start_time
        for _ in range(num_rows):
            # isoformat(timespec='seconds') + 'Z' is significantly faster than strftime
            # It produces the exact same format: YYYY-MM-DDTHH:MM:SSZ
            ts = curr_dt.isoformat(timespec='seconds') + 'Z'
            yield [
                ts,
                choice(sensor_ids),
                round_val(uniform(-20.0, 50.0), 2),
                choice(statuses)
            ]
            curr_dt += delta

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "sensor_id", "temperature", "status"])
        # Use writerows with a generator for efficient batch writing
        writer.writerows(data_generator())

if __name__ == "__main__":
    print("Generating 500k rows of sensor data...")
    generate_csv("sensor_data.csv")
    print("Data generation complete.")
