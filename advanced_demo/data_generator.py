import csv
import random
from datetime import datetime, timedelta

def generate_csv(filename: str, num_rows: int = 500000):
    start_time = datetime(2026, 1, 1)
    statuses = ["active", "inactive", "error"]
    # Pre-generate sensor ID strings to avoid formatting in the loop
    sensor_ids = [f"sensor_{i}" for i in range(1, 1001)]
    delta = timedelta(minutes=1)
    
    # Local references for faster method access
    choice = random.choice
    uniform = random.uniform
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "sensor_id", "temperature", "status"])
        
        def row_generator():
            curr_dt = start_time
            for _ in range(num_rows):
                # isoformat() is significantly faster than strftime()
                # Yielding a tuple is slightly more efficient than a list
                yield (
                    curr_dt.isoformat() + "Z",
                    choice(sensor_ids),
                    round(uniform(-20.0, 50.0), 2),
                    choice(statuses)
                )
                curr_dt += delta
        
        # writerows with a generator reduces Python-to-C overhead for I/O
        writer.writerows(row_generator())

if __name__ == "__main__":
    print("Generating 500k rows of sensor data...")
    generate_csv("sensor_data.csv")
    print("Data generation complete.")
