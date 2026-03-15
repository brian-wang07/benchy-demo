import json
import random
import uuid

def generate_mock_data(num_users=1000, num_transactions=5000):
    # Cache functions to local variables for faster access in loops
    _uuid4 = uuid.uuid4
    _randint = random.randint
    _uniform = random.uniform
    _round = round
    _choice = random.choice
    
    user_ids = []
    
    # Optimize User generation: Single pass and buffered I/O
    with open("users.jsonl", "w") as f:
        buffer = []
        for _ in range(num_users):
            uid = str(_uuid4())
            user_ids.append(uid)
            # Using f-strings instead of json.dumps for known safe alphanumeric data
            u_str = f'{{"id": "{uid}", "name": "User_{_randint(1, 10000)}", "email": "user{_randint(1, 10000)}@example.com"}}'
            buffer.append(u_str)
            
            if len(buffer) >= 1000:
                f.write("\n".join(buffer) + "\n")
                buffer = []
        if buffer:
            f.write("\n".join(buffer) + "\n")

    # Optimize Transaction generation: Stream writing to fix memory bottleneck
    with open("transactions.json", "w") as f:
        f.write("[")
        
        last_idx = num_transactions - 1
        for i in range(num_transactions):
            uid = _choice(user_ids)
            amt = _round(_uniform(5.0, 500.0), 2)
            
            # Manually construct JSON to match `indent=2` exactly without the overhead of json.dumps
            # This maintains exact functional parity for the specific data types used.
            t_str = (
                f'\n  {{\n'
                f'    "id": "{_uuid4()}",\n'
                f'    "user_id": "{uid}",\n'
                f'    "amount": {amt},\n'
                f'    "timestamp": "2026-03-14T12:00:00Z"\n'
                f'  }}'
            )
            
            if i < last_idx:
                f.write(t_str + ",")
            else:
                f.write(t_str)
        
        if num_transactions > 0:
            f.write("\n")
        f.write("]")

if __name__ == "__main__":
    print("Generating mock data...")
    generate_mock_data(2000, 10000)
    print("Done generating users.jsonl and transactions.json")
