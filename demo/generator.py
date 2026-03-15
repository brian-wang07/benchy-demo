import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    import uuid
    import random
    
    # Local variable caching for maximum performance in hot loops
    _uuid4 = uuid.uuid4
    _randint = random.randint
    _uniform = random.uniform
    _choices = random.choices
    _str = str

    # Generate user IDs once - needed for random.choices later
    user_ids = [_str(_uuid4()) for _ in range(num_users)]
    
    # Write users.jsonl using manual string formatting for speed
    with open("users.jsonl", "w") as f:
        for user_id in user_ids:
            # Replicating json.dumps(dict) format: {"id": "...", "name": "...", "email": "..."}
            f.write(f'{{"id": "{user_id}", "name": "User_{_randint(1, 10000)}", "email": "user{_randint(1, 10000)}@example.com"}}\\n')

    # Pick users for transactions
    if num_transactions == 0:
        with open("transactions.json", "w") as f:
            f.write("[]")
        return

    chosen_users = _choices(user_ids, k=num_transactions)
    
    # Stream transactions to file to maintain O(1) memory and maximize speed
    with open("transactions.json", "w") as f:
        f.write("[\\n")
        
        last_idx = num_transactions - 1
        ts = "2026-03-14T12:00:00Z" # Constant string
        
        for i, uid in enumerate(chosen_users):
            tid = _uuid4()
            amt = round(_uniform(5.0, 500.0), 2)
            
            # Manual formatting to match json.dump(indent=2) exactly
            # This is significantly faster than calling json.dumps() repeatedly
            block = (
                f'  {{\\n'
                f'    "id": "{tid}",\\n'
                f'    "user_id": "{uid}",\\n'
                f'    "amount": {amt},\\n'
                f'    "timestamp": "{ts}"\\n'
                f'  }}'
            )
            
            if i < last_idx:
                f.write(block + ",\\n")
            else:
                f.write(block + "\\n")
                
        f.write("]")

if __name__ == "__main__":
    print("Generating mock data...")
    generate_mock_data(2000, 10000)
    print("Done generating users.jsonl and transactions.json")
