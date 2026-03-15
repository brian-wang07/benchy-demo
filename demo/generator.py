import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    _uuid4 = uuid.uuid4
    _randint = random.randint
    _uniform = random.uniform
    _round = round

    user_ids = [str(_uuid4()) for _ in range(num_users)]
    
    with open("users.jsonl", "w") as f:
        for user_id in user_ids:
            # Using f-string for speed; matches json.dumps() formatting for this structure
            f.write(f'{{"id": "{user_id}", "name": "User_{_randint(1, 10000)}", "email": "user{_randint(1, 10000)}@example.com"}}\\n')

    chosen_users = random.choices(user_ids, k=num_transactions)
    
    with open("transactions.json", "w") as f:
        if not chosen_users:
            f.write("[]")
            return

        f.write("[\\n")
        last_idx = num_transactions - 1
        for i, uid in enumerate(chosen_users):
            tid = str(_uuid4())
            amount = _round(_uniform(5.0, 500.0), 2)
            # Manually constructing the JSON block to match indent=2 parity without O(N) memory
            t_str = (
                f'  {{\\n'
                f'    "id": "{tid}",\\n'
                f'    "user_id": "{uid}",\\n'
                f'    "amount": {amount},\\n'
                f'    "timestamp": "2026-03-14T12:00:00Z"\\n'
                f'  }}'
            )
            f.write(t_str)
            if i < last_idx:
                f.write(",\\n")
            else:
                f.write("\\n")
        f.write("]")

if __name__ == "__main__":
    print("Generating mock data...")
    generate_mock_data(2000, 10000)
    print("Done generating users.jsonl and transactions.json")
