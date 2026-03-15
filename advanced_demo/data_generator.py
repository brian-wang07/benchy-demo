import csv
import random
from datetime import datetime, timedelta

def generate_csv(filename: str, num_rows: int = 500000):
    start_time = datetime(2026, 1, 1)
    statuses = ["active", "inactive", "error"]
    # Pre-calculate sensor IDs to avoid f-string formatting in the loop
    sensor_ids = [f"sensor_{i}" for i in range(1, 1001)]
    
    # Bulk-generate random selections for sensor IDs and statuses
    # This is significantly faster than calling random.choice in every iteration
    s_ids = random.choices(sensor_ids, k=num_rows)
    st_vals = random.choices(statuses, k=num_rows)
    
    # Localize functions for faster access
    td = timedelta(minutes=1)
    runiform = random.uniform
    rround = round

    def row_generator():
        curr = start_time
        for i in range(num_rows):
            # isoformat + "Z" is much faster than strftime
            ts = curr.isoformat(timespec='seconds') + "Z"
            # Temperature still needs unique random value per row
            temp = rround(runiform(-20.0, 50.0), 2)
            
            yield (ts, s_ids[i], temp, st_vals[i])
            curr += td

    with open(filename, 'w', newline='', buffering=65536) as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "sensor_id", "temperature", "status"])
        # writerows with a generator reduces Python-to-C overhead
        writer.writerows(row_generator())

if __name__ == "__main__":
    print("Generating 500k rows of sensor data...")
    generate_csv("sensor_data.csv")
    print("Data generation complete.")
