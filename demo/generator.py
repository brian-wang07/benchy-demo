import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    # Keep as UUID objects to avoid early string conversion overhead
    user_ids = [uuid.uuid4() for _ in range(num_users)]
    
    with open("users.jsonl", "w") as f:
        for user_id in user_ids:
            # Use f-strings for JSONL to avoid json.dumps overhead
            # Parity: name and email use different random integers
            u_str = (f'{{"id": "{user_id}", '
                     f'"name": "User_{random.randint(1, 10000)}", '
                     f'"email": "user{random.randint(1, 10000)}@example.com"}}\n')
            f.write(u_str)

    if num_transactions == 0:
        with open("transactions.json", "w") as f:
            f.write("[]")
        return

    chosen_users = random.choices(user_ids, k=num_transactions)
    
    with open("transactions.json", "w") as f:
        f.write("[\n")
        last_idx = num_transactions - 1
        for i, uid in enumerate(chosen_users):
            # Generate transaction data directly into a string
            # Parity: matches json.dump(indent=2) structure exactly
            tid = uuid.uuid4()
            amt = round(random.uniform(5.0, 500.0), 2)
            comma = "," if i < last_idx else ""
            
            t_str = (f'  {{\n'
                     f'    "id": "{tid}",\n'
                     f'    "user_id": "{uid}",\n'
                     f'    "amount": {amt},\n'
                     f'    "timestamp": "2026-03-14T12:00:00Z"\n'
                     f'  }}{comma}\n')
            f.write(t_str)
        f.write("]")

if __name__ == "__main__":
    print("Generating mock data...")
    generate_mock_data(2000, 10000)
    print("Done generating users.jsonl and transactions.json")
