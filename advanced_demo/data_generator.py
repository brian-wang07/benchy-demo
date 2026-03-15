import csv
import random
from datetime import datetime, timedelta

def generate_csv(filename: str, num_rows: int = 500000):
    start_time = datetime(2026, 1, 1)
    statuses = ["active", "inactive", "error"]
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "sensor_id", "temperature", "status"])
        batch = []
        batch_size = 10000
        dt = start_time
        delta = timedelta(minutes=1)
        
        for _ in range(num_rows):
            # Fixed ISO8601 format
            ts = f"{dt.year:04d}-{dt.month:02d}-{dt.day:02d}T{dt.hour:02d}:{dt.minute:02d}:00Z"
            sensor_id = f"sensor_{random.randint(1, 1000)}"
            temp = round(random.uniform(-20.0, 50.0), 2)
            status = random.choice(statuses)
            batch.append([ts, sensor_id, temp, status])
            
            if len(batch) >= batch_size:
                writer.writerows(batch)
                batch.clear()
                
            dt += delta
            
        if batch:
            writer.writerows(batch)

if __name__ == "__main__":
    print("Generating 500k rows of sensor data...")
    generate_csv("sensor_data.csv")
    print("Data generation complete.")
