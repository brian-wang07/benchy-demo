import csv
import random
from datetime import datetime, timedelta

def generate_csv(filename: str, num_rows: int = 500000):
    start_time = datetime(2026, 1, 1)
    statuses = ["active", "inactive", "error"]
    sensor_ids = [f"sensor_{i}" for i in range(1, 1001)]
    
    # Cache functions for tight loop
    rand_uniform = random.uniform
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "sensor_id", "temperature", "status"])
        
        batch_size = 10000
        dt = start_time
        minute_delta = timedelta(minutes=1)
        
        for i in range(0, num_rows, batch_size):
            chunk_size = min(batch_size, num_rows - i)
            
            s_ids = random.choices(sensor_ids, k=chunk_size)
            st_batch = random.choices(statuses, k=chunk_size)
            
            batch = []
            append = batch.append
            for j in range(chunk_size):
                ts = dt.isoformat(timespec='seconds') + "Z"
                temp = round(rand_uniform(-20.0, 50.0), 2)
                append([ts, s_ids[j], temp, st_batch[j]])
                dt += minute_delta
                
            writer.writerows(batch)

if __name__ == "__main__":
    print("Generating 500k rows of sensor data...")
    generate_csv("sensor_data.csv")
    print("Data generation complete.")
