import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    user_ids = [str(uuid.uuid4()) for _ in range(num_users)]
    
    with open("users.jsonl", "w") as f:
        for user_id in user_ids:
            # Direct string formatting is significantly faster than json.dumps for fixed schemas
            name = f"User_{random.randint(1, 10000)}"
            email = f"user{random.randint(1,10000)}@example.com"
            f.write(f'{{"id": "{user_id}", "name": "{name}", "email": "{email}"}}\n')

    # random.choices is efficient for pre-selecting users
    chosen_users = random.choices(user_ids, k=num_transactions)
    
    # Streaming to disk with manual formatting matches json.dump(indent=2) exactly 
    # but avoids O(N) memory and expensive object serialization logic.
    with open("transactions.json", "w") as f:
        f.write("[\n")
        last_idx = num_transactions - 1
        for i, uid in enumerate(chosen_users):
            txn_id = uuid.uuid4()
            amt = round(random.uniform(5.0, 500.0), 2)
            comma = "," if i < last_idx else ""
            f.write(f'  {{\n    "id": "{txn_id}",\n    "user_id": "{uid}",\n    "amount": {amt},\n    "timestamp": "2026-03-14T12:00:00Z"\n  }}{comma}\n')
        f.write("]")

if __name__ == "__main__":
    print("Generating mock data...")
    generate_mock_data(2000, 10000)
    print("Done generating users.jsonl and transactions.json")
