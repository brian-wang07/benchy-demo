import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    uuid4 = uuid.uuid4
    randint = random.randint
    uniform = random.uniform

    user_ids = [str(uuid4()) for _ in range(num_users)]
    
    user_lines = [
        f'{{"id": "{uid}", "name": "User_{randint(1, 10000)}", "email": "user{randint(1, 10000)}@example.com"}}\n'
        for uid in user_ids
    ]
    
    with open("users.jsonl", "w") as f:
        f.writelines(user_lines)

    chosen_users = random.choices(user_ids, k=num_transactions)
    transactions = [
        {
            "id": str(uuid4()),
            "user_id": uid,
            "amount": round(uniform(5.0, 500.0), 2),
            "timestamp": "2026-03-14T12:00:00Z"
        }
        for uid in chosen_users
    ]
    
    with open("transactions.json", "w") as f:
        json.dump(transactions, f, indent=2)

if __name__ == "__main__":
    print("Generating mock data...")
    generate_mock_data(2000, 10000)
    print("Done generating users.jsonl and transactions.json")
