import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    # Bind functions to local variables for performance
    uuid4 = uuid.uuid4
    randint = random.randint
    uniform = random.uniform
    
    # Generate user IDs using the standard uuid4 to ensure fingerprint parity.
    # We use str() on the UUID object as it is the standard representation.
    user_ids = [str(uuid4()) for _ in range(num_users)]
    
    # Efficiently write users.jsonl using manual string formatting.
    # This avoids the overhead of the json module while maintaining exact output format.
    with open("users.jsonl", "w") as f:
        # Standard json.dumps() for these small dicts follows this specific pattern.
        # We interleave randint calls exactly as the original to preserve PRNG state.
        user_lines = [
            '{"id": "%s", "name": "User_%d", "email": "user%d@example.com"}\n' % (uid, randint(1, 10000), randint(1, 10000))
            for uid in user_ids
        ]
        f.writelines(user_lines)

    # random.choices is efficient for bulk selection.
    chosen_users = random.choices(user_ids, k=num_transactions)
    
    # Use a list comprehension for bulk transaction generation.
    # This matches the original's call order for uuid4 and uniform.
    transactions = [
        {
            "id": str(uuid4()),
            "user_id": uid,
            "amount": round(uniform(5.0, 500.0), 2),
            "timestamp": "2026-03-14T12:00:00Z"
        }
        for uid in chosen_users
    ]
    
    # json.dump is necessary here to maintain the exact 'indent=2' formatting.
    with open("transactions.json", "w") as f:
        json.dump(transactions, f, indent=2)

if __name__ == "__main__":
    print("Generating mock data...")
    generate_mock_data(2000, 10000)
    print("Done generating users.jsonl and transactions.json")
