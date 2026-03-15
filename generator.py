import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    user_ids = []
    
    with open("users.jsonl", "w") as f:
        for _ in range(num_users):
            user_id = str(uuid.uuid4())
            user_ids.append(user_id)
            name_idx = random.randint(1, 10000)
            email_idx = random.randint(1, 10000)
            f.write(f'{{"id": "{user_id}", "name": "User_{name_idx}", "email": "user{email_idx}@example.com"}}\n')

    with open("transactions.json", "w") as f:
        if num_transactions == 0:
            f.write("[]")
        else:
            f.write("[\n")
            for i in range(num_transactions):
                t_id = str(uuid.uuid4())
                u_id = random.choice(user_ids)
                amount = round(random.uniform(5.0, 500.0), 2)
                t_str = (
                    "  {\n"
                    f'    "id": "{t_id}",\n'
                    f'    "user_id": "{u_id}",\n'
                    f'    "amount": {amount},\n'
                    '    "timestamp": "2026-03-14T12:00:00Z"\n'
                    "  }"
                )
                f.write(t_str)
                if i < num_transactions - 1:
                    f.write(",\n")
                else:
                    f.write("\n")
            f.write("]")

if __name__ == "__main__":
    print("Generating mock data...")
    generate_mock_data(2000, 10000)
    print("Done generating users.jsonl and transactions.json")
