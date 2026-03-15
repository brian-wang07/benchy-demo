import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    _uuid4 = uuid.uuid4
    _str = str
    _randint = random.randint
    _uniform = random.uniform
    _round = round

    user_ids = []
    # Stream users.jsonl and collect user_ids in one pass
    with open("users.jsonl", "w") as f:
        for _ in range(num_users):
            uid = _str(_uuid4())
            user_ids.append(uid)
            # Match json.dumps default formatting (separators=(', ', ': '))
            f.write(f'{{"id": "{uid}", "name": "User_{_randint(1, 10000)}", "email": "user{_randint(1, 10000)}@example.com"}}\n')

    if num_transactions == 0:
        with open("transactions.json", "w") as f:
            f.write("[]")
        return

    chosen_users = random.choices(user_ids, k=num_transactions)
    
    with open("transactions.json", "w") as f:
        f.write("[\n")
        last_idx = num_transactions - 1
        buffer = []
        for i, uid in enumerate(chosen_users):
            tx_id = _str(_uuid4())
            amount = _round(_uniform(5.0, 500.0), 2)
            comma = ",\n" if i < last_idx else ""
            
            # Match json.dump(indent=2) format exactly
            entry = (
                f'  {{\n'
                f'    "id": "{tx_id}",\n'
                f'    "user_id": "{uid}",\n'
                f'    "amount": {amount},\n'
                f'    "timestamp": "2026-03-14T12:00:00Z"\n'
                f'  }}{comma}'
            )
            buffer.append(entry)
            
            # Batch writes for performance
            if len(buffer) >= 1000:
                f.write("".join(buffer))
                buffer.clear()
        
        if buffer:
            f.write("".join(buffer))
        f.write("\n]")

if __name__ == "__main__":
    print("Generating mock data...")
    generate_mock_data(2000, 10000)
    print("Done generating users.jsonl and transactions.json")
