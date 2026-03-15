import csv
import random
from datetime import datetime, timedelta

def generate_csv(filename: str, num_rows: int = 500000):
    start_time = datetime(2026, 1, 1)
    statuses = ["active", "inactive", "error"]
    sensor_ids = [f"sensor_{i}" for i in range(1, 1001)]
    chunk_size = 10000
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "sensor_id", "temperature", "status"])
        
        dt = start_time
        delta = timedelta(minutes=1)
        
        for chunk_start in range(0, num_rows, chunk_size):
            current_chunk_size = min(chunk_size, num_rows - chunk_start)
            chunk_statuses = random.choices(statuses, k=current_chunk_size)
            chunk_sensors = random.choices(sensor_ids, k=current_chunk_size)
            
            chunk = []
            for j in range(current_chunk_size):
                # Fixed ISO8601 format
                ts = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                temp = round(random.uniform(-20.0, 50.0), 2)
                chunk.append([ts, chunk_sensors[j], temp, chunk_statuses[j]])
                dt += delta
            
            writer.writerows(chunk)

if __name__ == "__main__":
    print("Generating 500k rows of sensor data...")
    generate_csv("sensor_data.csv")
    print("Data generation complete.")
