import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    user_ids = []
    with open("users.jsonl", "w") as f:
        for _ in range(num_users):
            u_id = str(uuid.uuid4())
            user_ids.append(u_id)
            u = {
                "id": u_id,
                "name": f"User_{random.randint(1, 10000)}",
                "email": f"user{random.randint(1,10000)}@example.com"
            }
            f.write(json.dumps(u) + "\n")

    with open("transactions.json", "w") as f:
        if num_transactions == 0:
            f.write("[]")
        else:
            f.write("[\n")
            for i in range(num_transactions):
                t = {
                    "id": str(uuid.uuid4()),
                    "user_id": random.choice(user_ids),
                    "amount": round(random.uniform(5.0, 500.0), 2),
                    "timestamp": "2026-03-14T12:00:00Z"
                }
                t_str = "  " + json.dumps(t, indent=2).replace("\n", "\n  ")
                if i < num_transactions - 1:
                    f.write(t_str + ",\n")
                else:
                    f.write(t_str + "\n")
            f.write("]")

if __name__ == "__main__":
    print("Generating mock data...")
    generate_mock_data(2000, 10000)
    print("Done generating users.jsonl and transactions.json")
