import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    user_ids = [str(uuid.uuid4()) for _ in range(num_users)]
    
    with open("users.jsonl", "w") as f:
        for user_id in user_ids:
            u = {
                "id": user_id,
                "name": f"User_{random.randint(1, 10000)}",
                "email": f"user{random.randint(1,10000)}@example.com"
            }
            f.write(json.dumps(u) + "\n")

    chosen_users = random.choices(user_ids, k=num_transactions)
    
    with open("transactions.json", "w") as f:
        f.write("[\n")
        for i, uid in enumerate(chosen_users):
            amount = round(random.uniform(5.0, 500.0), 2)
            t_str = f'  {{\n    "id": "{str(uuid.uuid4())}",\n    "user_id": "{uid}",\n    "amount": {amount},\n    "timestamp": "2026-03-14T12:00:00Z"\n  }}'
            if i > 0:
                f.write(",\n")
            f.write(t_str)
        f.write("\n]\n")

if __name__ == "__main__":
    print("Generating mock data...")
    generate_mock_data(2000, 10000)
    print("Done generating users.jsonl and transactions.json")
