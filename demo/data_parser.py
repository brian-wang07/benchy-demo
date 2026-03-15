import json

def load_transactions(filepath):
    """
    Loads transactions from a JSON file.
    Optimized: Reads the entire file into memory as bytes and parses in one go.
    """
    with open(filepath, 'rb') as f:
        return json.loads(f.read())

def load_users(filepath):
    """
    Loads users from a JSONL file.
    Optimized: Uses map() for faster iteration and binary read for lower overhead.
    """
    with open(filepath, 'rb') as f:
        return list(map(json.loads, f))
