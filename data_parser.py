import json

def load_transactions(filepath):
    """
    Loads transactions from a JSON file.
    Intentional bottleneck: Reads the entire file into a giant string first.
    """
    with open(filepath, 'r') as f:
        # Memory bottleneck: reading everything into memory at once
        raw_data = f.read()
    
    data = json.loads(raw_data)
    return data

def load_users(filepath):
    """
    Loads users from a JSONL file.
    Intentional bottleneck: Uses readlines() which loads all lines into memory.
    """
    with open(filepath, 'r') as f:
        # Memory bottleneck: readlines creates a huge list of strings in memory
        lines = f.readlines()
    
    users = []
    for line in lines:
        users.append(json.loads(line))
    return users
