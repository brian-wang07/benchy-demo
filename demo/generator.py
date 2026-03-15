import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    user_ids = [str(uuid.uuid4()) for _ in range(num_users)]
    
    with open("users.jsonl", "w") as f:
        batch = []
        for user_id in user_ids:
            # Using f-strings and batching is faster than json.dumps in a loop
            # This maintains the exact format of json.dumps (including space after colon)
            line = f'{{"id": "{user_id}", "name": "User_{random.randint(1, 10000)}", "email": "user{random.randint(1, 10000)}@example.com"}}\n'
            batch.append(line)
            if len(batch) >= 1000:
                f.write("".join(batch))
                batch = []
        if batch:
            f.write("".join(batch))

    if num_transactions == 0:
        with open("transactions.json", "w") as f:
            f.write("[]")
        return

    chosen_users = random.choices(user_ids, k=num_transactions)
    
    with open("transactions.json", "w") as f:
        f.write("[\n")
        batch = []
        last_idx = num_transactions - 1
        for i, uid in enumerate(chosen_users):
            tid = str(uuid.uuid4())
            amt = round(random.uniform(5.0, 500.0), 2)
            
            # Manually construct the indented JSON string to match json.dump(indent=2)
            # This avoids the overhead of dictionary creation and the json serializer
            item = (
                f'  {{\n'
                f'    "id": "{tid}",\n'
                f'    "user_id": "{uid}",\n'
                f'    "amount": {amt},\n'
                f'    "timestamp": "2026-03-14T12:00:00Z"\n'
                f'  }}'
            )
            
            if i < last_idx:
                batch.append(item + ",\n")
            else:
                batch.append(item + "\n")
            
            if len(batch) >= 1000:
                f.write("".join(batch))
                batch = []
        
        if batch:
            f.write("".join(batch))
        f.write("]")

if __name__ == "__main__":
    print("Generating mock data...")
    generate_mock_data(2000, 10000)
    print("Done generating users.jsonl and transactions.json")
