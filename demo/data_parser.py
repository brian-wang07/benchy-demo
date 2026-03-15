import json

def load_transactions(filepath):
    """
    Loads transactions from a JSON file.
    Optimized for speed by reading the entire file as bytes into memory first.
    """
    with open(filepath, 'rb') as f:
        data = json.loads(f.read())
    return data

def load_users(filepath):
    """
    Loads users from a JSONL file.
    Optimized for speed using a C-level map loop and binary file reading.
    """
    with open(filepath, 'rb') as f:
        users = list(map(json.loads, f))
    return users
