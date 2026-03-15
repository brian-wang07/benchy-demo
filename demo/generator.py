import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    user_ids = [str(uuid.uuid4()) for _ in range(num_users)]
    
    with open("users.jsonl", "w") as f:
        for user_id in user_ids:
            name = f"User_{random.randint(1, 10000)}"
            email = f"user{random.randint(1,10000)}@example.com"
            f.write(f'{{"id": "{user_id}", "name": "{name}", "email": "{email}"}}\n')

    chosen_users = random.choices(user_ids, k=num_transactions)
    
    with open("transactions.json", "w") as f:
        f.write("[\n")
        last_idx = num_transactions - 1
        for i, uid in enumerate(chosen_users):
            t_id = str(uuid.uuid4())
            amount = round(random.uniform(5.0, 500.0), 2)
            f.write(f'''  {{
    "id": "{t_id}",
    "user_id": "{uid}",
    "amount": {amount},
    "timestamp": "2026-03-14T12:00:00Z"
  }}''')
            if i != last_idx:
                f.write(",\n")
            else:
                f.write("\n")
        f.write("]")

if __name__ == "__main__":
    print("Generating mock data...")
    generate_mock_data(2000, 10000)
    print("Done generating users.jsonl and transactions.json")
