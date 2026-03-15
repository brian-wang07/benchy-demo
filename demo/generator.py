import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    uuid4 = uuid.uuid4
    randint = random.randint
    uniform = random.uniform

    user_ids = [str(uuid4()) for _ in range(num_users)]
    
    with open("users.jsonl", "w") as f:
        chunk_size = 1000
        for i in range(0, num_users, chunk_size):
            chunk_data = [
                f'{{"id": "{uid}", "name": "User_{randint(1, 10000)}", "email": "user{randint(1,10000)}@example.com"}}'
                for uid in user_ids[i:i+chunk_size]
            ]
            f.write("\n".join(chunk_data) + "\n")

    chosen_users = random.choices(user_ids, k=num_transactions)
    
    if num_transactions == 0:
        with open("transactions.json", "w") as f:
            f.write("[]")
    else:
        with open("transactions.json", "w") as f:
            f.write("[\n")
            chunk_size = 1000
            for i in range(0, num_transactions, chunk_size):
                chunk = chosen_users[i:i+chunk_size]
                chunk_data = [
                    f'  {{\n    "id": "{str(uuid4())}",\n    "user_id": "{uid}",\n    "amount": {round(uniform(5.0, 500.0), 2)},\n    "timestamp": "2026-03-14T12:00:00Z"\n  }}'
                    for uid in chunk
                ]
                if i > 0 and chunk_data:
                    f.write(",\n")
                f.write(",\n".join(chunk_data))
            f.write("\n]")

if __name__ == "__main__":
    print("Generating mock data...")
    generate_mock_data(2000, 10000)
    print("Done generating users.jsonl and transactions.json")
