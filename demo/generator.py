import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    # Pre-cache functions to local variables for faster lookup in loops
    _uuid4 = uuid.uuid4
    _randint = random.randint
    _dumps = json.dumps

    user_ids = [str(_uuid4()) for _ in range(num_users)]
    
    # Use a generator and join for faster bulk writing of jsonl
    with open("users.jsonl", "w") as f:
        user_lines = (
            _dumps({
                "id": uid,
                "name": f"User_{_randint(1, 10000)}",
                "email": f"user{_randint(1, 10000)}@example.com"
            }) for uid in user_ids
        )
        f.write("\n".join(user_lines) + "\n")

    chosen_users = random.choices(user_ids, k=num_transactions)
    
    _uniform = random.uniform
    _round = round
    ts = "2026-03-14T12:00:00Z" # Pre-calculate constant string
    
    transactions = [
        {
            "id": str(_uuid4()),
            "user_id": uid,
            "amount": _round(_uniform(5.0, 500.0), 2),
            "timestamp": ts
        }
        for uid in chosen_users
    ]
    
    # Optimized serialization by removing indentation and using compact separators
    with open("transactions.json", "w") as f:
        json.dump(transactions, f, separators=(',', ':'))

if __name__ == "__main__":
    print("Generating mock data...")
    generate_mock_data(2000, 10000)
    print("Done generating users.jsonl and transactions.json")
