import json
import random
import os

def generate_db(filename="db.json"):
    print("Generating mock database. This might take a second...")
    data = {
        "users": {},
        "transactions": {}
    }
    users = data["users"]
    transactions = data["transactions"]
    
    # Cache methods locally for faster access in the hot loop
    runif = random.uniform
    rnd = round

    for i in range(2000):
        user_id = f"user_{i}"
        tx_ids = [None] * 20  # Pre-allocate list to avoid resizing
        
        users[user_id] = {
            "name": f"User {i}", 
            "email": f"user{i}@example.com",
            "transactions": tx_ids
        }
        
        # Single pass: populate both the list of IDs and the transaction details
        for j in range(20):
            tx_id = f"tx_{i}_{j}"
            tx_ids[j] = tx_id
            transactions[tx_id] = {
                "id": tx_id,
                "amount": rnd(runif(10, 500), 2), 
                "status": "completed"
            }
             
    with open(filename, "w") as f:
        json.dump(data, f)
    
    file_size_mb = os.path.getsize(filename) / 1024 / 1024
    print(f"Generated {filename} with size: {file_size_mb:.2f} MB")

if __name__ == "__main__":
    generate_db()
