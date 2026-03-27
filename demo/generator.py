import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    user_ids = [str(uuid.uuid4()) for _ in range(num_users)]
    
    # Pre-calculate constants for speed
    _randint = random.randint
    _uniform = random.uniform
    _round = round
    _uuid4 = uuid.uuid4

    with open("users.jsonl", "w") as f:
        # Use a generator to avoid dict overhead; manual f-string for max speed
        for uid in user_ids:
            f.write(f'{{"id": "{uid}", "name": "User_{_randint(1, 10000)}", "email": "user{_randint(1, 10000)}@example.com"}}\n')

    if num_transactions == 0:
        with open("transactions.json", "w") as f:
            f.write("[]")
        return

    chosen_users = random.choices(user_ids, k=num_transactions)
    timestamp = "2026-03-14T12:00:00Z"
    
    with open("transactions.json", "w") as f:
        f.write("[\n")
        last_idx = num_transactions - 1
        for i, uid in enumerate(chosen_users):
            # Manual construction of the JSON object string to match `indent=2` perfectly
            # This is significantly faster than json.dumps() for known structures.
            txn_str = (
                '  {\n'
                f'    "id": "{_uuid4()}",\n'
                f'    "user_id": "{uid}",\n'
                f'    "amount": {_round(_uniform(5.0, 500.0), 2)},\n'
                f'    "timestamp": "{timestamp}"\n'
                '  }'
            )
            f.write(txn_str)
            if i < last_idx:
                f.write(",\n")
            else:
                f.write("\n")
        f.write("]")

if __name__ == "__main__":
    print("Generating mock data...")
    generate_mock_data(2000, 10000)
    print("Done generating users.jsonl and transactions.json")
