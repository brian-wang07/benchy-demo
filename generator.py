import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    user_ids = []
    # Stream users to file and store only IDs in memory
    with open("users.jsonl", "w") as f:
        for _ in range(num_users):
            uid = str(uuid.uuid4())
            user = {
                "id": uid,
                "name": f"User_{random.randint(1, 10000)}",
                "email": f"user{random.randint(1,10000)}@example.com"
            }
            f.write(json.dumps(user) + "\n")
            user_ids.append(uid)

    # Stream transactions directly to file as a JSON array
    with open("transactions.json", "w") as f:
        if num_transactions == 0:
            f.write("[]")
        else:
            f.write("[\n")
            for i in range(num_transactions):
                transaction = {
                    "id": str(uuid.uuid4()),
                    "user_id": random.choice(user_ids),
                    "amount": round(random.uniform(5.0, 500.0), 2),
                    "timestamp": "2026-03-14T12:00:00Z"
                }
                # Manually format to match indent=2 parity
                serialized = json.dumps(transaction, indent=2)
                f.write("  " + serialized.replace("\n", "\n  "))
                
                if i < num_transactions - 1:
                    f.write(",\n")
                else:
                    f.write("\n")
            f.write("]")

if __name__ == "__main__":
    print("Generating mock data...")
    generate_mock_data(2000, 10000)
    print("Done generating users.jsonl and transactions.json")
