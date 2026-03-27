import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    user_ids = [str(uuid.uuid4()) for _ in range(num_users)]
    
    # Speed optimization: Use f-strings and buffered writes instead of json.dumps in a loop
    with open("users.jsonl", "w") as f:
        user_buffer = []
        for user_id in user_ids:
            u_str = f'{{"id": "{user_id}", "name": "User_{random.randint(1, 10000)}", "email": "user{random.randint(1, 10000)}@example.com"}}\n'
            user_buffer.append(u_str)
            if len(user_buffer) >= 1000:
                f.write("".join(user_buffer))
                user_buffer = []
        f.write("".join(user_buffer))

    chosen_users = random.choices(user_ids, k=num_transactions)
    
    # Memory optimization: Stream transactions to file to avoid O(N) list of dicts.
    # Speed optimization: Manual f-string formatting for JSON to bypass heavy json.dumps logic.
    with open("transactions.json", "w") as f:
        f.write("[\n")
        txn_buffer = []
        last_idx = num_transactions - 1
        for i, uid in enumerate(chosen_users):
            txn_id = str(uuid.uuid4())
            amount = round(random.uniform(5.0, 500.0), 2)
            comma = "," if i < last_idx else ""
            
            # Match original indent=2 structure exactly
            txn_str = (
                f'  {{\n'
                f'    "id": "{txn_id}",\n'
                f'    "user_id": "{uid}",\n'
                f'    "amount": {amount},\n'
                f'    "timestamp": "2026-03-14T12:00:00Z"\n'
                f'  }}{comma}\n'
            )
            txn_buffer.append(txn_str)
            
            # Batch write to disk for performance
            if len(txn_buffer) >= 1000:
                f.write("".join(txn_buffer))
                txn_buffer = []
        
        if txn_buffer:
            f.write("".join(txn_buffer))
        f.write("]")

if __name__ == "__main__":
    print("Generating mock data...")
    generate_mock_data(2000, 10000)
    print("Done generating users.jsonl and transactions.json")
