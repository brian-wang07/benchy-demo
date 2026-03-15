import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    _uuid4 = uuid.uuid4
    _randint = random.randint
    _uniform = random.uniform
    
    user_ids = [str(_uuid4()) for _ in range(num_users)]
    
    users_json_lines = [
        json.dumps({
            "id": user_id,
            "name": f"User_{_randint(1, 10000)}",
            "email": f"user{_randint(1,10000)}@example.com"
        })
        for user_id in user_ids
    ]
    
    with open("users.jsonl", "w") as f:
        if users_json_lines:
            f.write("\n".join(users_json_lines) + "\n")

    chosen_users = random.choices(user_ids, k=num_transactions)
    transactions = [
        {
            "id": str(_uuid4()),
            "user_id": uid,
            "amount": round(_uniform(5.0, 500.0), 2),
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
