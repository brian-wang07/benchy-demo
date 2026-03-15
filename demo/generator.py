import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    # Cache functions locally for speed
    _uuid4 = uuid.uuid4
    _randint = random.randint
    _uniform = random.uniform
    _choices = random.choices
    _dumps = json.dumps

    user_ids = [str(_uuid4()) for _ in range(num_users)]
    
    with open("users.jsonl", "w") as f:
        for user_id in user_ids:
            u = {
                "id": user_id,
                "name": f"User_{_randint(1, 10000)}",
                "email": f"user{_randint(1, 10000)}@example.com"
            }
            f.write(_dumps(u) + "\n")

    chosen_users = _choices(user_ids, k=num_transactions)
    timestamp = "2026-03-14T12:00:00Z"
    
    with open("transactions.json", "w") as f:
        if not chosen_users:
            f.write("[]")
        else:
            f.write("[\n")
            last_idx = num_transactions - 1
            for i, uid in enumerate(chosen_users):
                tx = {
                    "id": str(_uuid4()),
                    "user_id": uid,
                    "amount": round(_uniform(5.0, 500.0), 2),
                    "timestamp": timestamp
                }
                
                # Maintain exact indent=2 parity
                # Serializing dict and prefixing lines to simulate array indentation
                serialized = _dumps(tx, indent=2)
                indented = "  " + serialized.replace("\n", "\n  ")
                f.write(indented)
                
                if i < last_idx:
                    f.write(",\n")
                else:
                    f.write("\n")
            f.write("]")

if __name__ == "__main__":
    print("Generating mock data...")
    generate_mock_data(2000, 10000)
    print("Done generating users.jsonl and transactions.json")
