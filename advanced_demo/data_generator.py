import json
import random
import os

def generate_db(filename="db.json"):
    print("Generating mock database. This might take a second...")
    
    # Localizing variables and functions for high-performance access in hot loops
    _randint = random.randint
    _range = range
    _status = "completed"
    
    users = {}
    transactions = {}
    
    # 2000 users, 20 transactions each
    for i in _range(2000):
        # Generate strings once and reuse them
        u_id = f"user_{i}"
        tx_ids = [f"tx_{i}_{j}" for j in _range(20)]
        
        users[u_id] = {
            "name": f"User {i}", 
            "email": f"user{i}@example.com",
            "transactions": tx_ids
        }
        
        # Directly populate the transactions dict using pre-generated IDs
        for tx_id in tx_ids:
             transactions[tx_id] = {
                 "id": tx_id,
                 "amount": _randint(1000, 50000) / 100.0, 
                 "status": _status
             }
             
    data = {
        "users": users,
        "transactions": transactions
    }
    
    with open(filename, "w") as f:
        # Using separators=(',', ':') removes whitespace, making the file smaller and faster to write/parse.
        # check_circular=False provides a small speedup by skipping reference cycle checks.
        json.dump(data, f, separators=(',', ':'), check_circular=False)
    
    file_size_mb = os.path.getsize(filename) / 1024 / 1024
    print(f"Generated {filename} with size: {file_size_mb:.2f} MB")

if __name__ == "__main__":
    generate_db()
