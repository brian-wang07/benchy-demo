import json

def load_transactions(filepath):
    """
    Loads transactions from a JSON file using fast binary I/O.
    """
    with open(filepath, 'rb') as f:
        return json.loads(f.read())

def load_users(filepath):
    """
    Loads users from a JSONL file using binary mapping for maximum speed.
    """
    with open(filepath, 'rb') as f:
        return list(map(json.loads, f))
