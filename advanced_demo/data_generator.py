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
    uniform = random.uniform
    # 2000 users, 20 transactions each
    for i in range(2000):
        tx_ids = []
        # Merge ID generation and transaction population into a single pass
        for j in range(20):
            tx_id = f"tx_{i}_{j}"
            tx_ids.append(tx_id)
            transactions[tx_id] = {
                "id": tx_id,
                "amount": round(uniform(10, 500), 2), 
                "status": "completed"
            }
        
        users[f"user_{i}"] = {
            "name": f"User {i}", 
            "email": f"user{i}@example.com",
            "transactions": tx_ids
        }
             
    with open(filename, "w") as f:
        json.dump(data, f)
    
    file_size_mb = os.path.getsize(filename) / 1024 / 1024
    print(f"Generated {filename} with size: {file_size_mb:.2f} MB")

if __name__ == "__main__":
    generate_db()
