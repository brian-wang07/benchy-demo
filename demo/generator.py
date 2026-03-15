import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    # Localize functions for faster access in loops
    _uuid4 = uuid.uuid4
    _randint = random.randint
    _uniform = random.uniform
    _round = round
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

    chosen_users = random.choices(user_ids, k=num_transactions)
    ts = "2026-03-14T12:00:00Z" # Constant timestamp

    # Use a generator to avoid O(N) memory footprint of the transaction list
    transactions_gen = (
        {
            "id": str(_uuid4()),
            "user_id": uid,
            "amount": _round(_uniform(5.0, 500.0), 2),
            "timestamp": ts
        }
        for uid in chosen_users
    )
    
    # Stream the generator to file with indent=2 for functional parity
    with open("transactions.json", "w") as f:
        encoder = json.JSONEncoder(indent=2)
        for chunk in encoder.iterencode(transactions_gen):
            f.write(chunk)

if __name__ == "__main__":
    print("Generating mock data...")
    generate_mock_data(2000, 10000)
    print("Done generating users.jsonl and transactions.json")
