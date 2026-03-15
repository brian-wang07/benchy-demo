import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    # Pre-generate user IDs
    user_ids = [str(uuid.uuid4()) for _ in range(num_users)]
    
    # Writing users.jsonl using streaming and f-strings for speed
    with open("users.jsonl", "w") as f:
        _randint = random.randint
        for user_id in user_ids:
            # F-string is significantly faster than dict creation + json.dumps
            # Structure matches json.dumps default separators (": ", ", ")
            f.write(f'{{"id": "{user_id}", "name": "User_{_randint(1, 10000)}", "email": "user{_randint(1, 10000)}@example.com"}}\n')

    # Efficiently sample users for transactions
    chosen_users = random.choices(user_ids, k=num_transactions)
    
    # Writing transactions.json using streaming to avoid O(N) memory pressure
    with open("transactions.json", "w") as f:
        if not chosen_users:
            f.write("[]")
            return

        f.write("[\n")
        _uuid4 = uuid.uuid4
        _uniform = random.uniform
        _round = round
        _timestamp = "2026-03-14T12:00:00Z"
        last_idx = num_transactions - 1
        
        for i, uid in enumerate(chosen_users):
            # amount = round(uniform, 2) matches JSON serialization for this range
            amount = _round(_uniform(5.0, 500.0), 2)
            
            # Manually construct the JSON block to match indent=2 exactly
            # This bypasses the overhead of the json module entirely
            f.write(f'  {{\n'
                    f'    "id": "{_uuid4()}",\n'
                    f'    "user_id": "{uid}",\n'
                    f'    "amount": {amount},\n'
                    f'    "timestamp": "{_timestamp}"\n'
                    f'  }}')
            
            if i != last_idx:
                f.write(",\n")
            else:
                f.write("\n")
        f.write("]")

if __name__ == "__main__":
    print("Generating mock data...")
    generate_mock_data(2000, 10000)
    print("Done generating users.jsonl and transactions.json")
