import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    users = []
    for _ in range(num_users):
        users.append({
            "id": str(uuid.uuid4()),
            "name": f"User_{random.randint(1, 10000)}",
            "email": f"user{random.randint(1,10000)}@example.com"
        })
    
    with open("users.jsonl", "w") as f:
        for u in users:
            f.write(json.dumps(u) + "\n")

    user_ids = [u["id"] for u in users]
    transactions = []
    for _ in range(num_transactions):
        transactions.append({
            "id": str(uuid.uuid4()),
            "user_id": random.choice(user_ids),
            "amount": round(random.uniform(5.0, 500.0), 2),
            "timestamp": "2026-03-14T12:00:00Z"
        })
    
    with open("transactions.json", "w") as f:
        json.dump(transactions, f)

if __name__ == "__main__":
    print("Generating mock data...")
    generate_mock_data(2000, 10000)
    print("Done generating users.jsonl and transactions.json")
