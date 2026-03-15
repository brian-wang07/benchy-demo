import json

def load_transactions(filepath):
    """
    Loads transactions from a JSON file.
    Optimized for speed: Single-shot binary read and parse.
    """
    with open(filepath, 'rb') as f:
        return json.loads(f.read())

def load_users(filepath):
    """
    Loads users from a JSONL file.
    Optimized for speed: Uses map for C-level iteration and binary reading.
    """
    with open(filepath, 'rb') as f:
        return list(map(json.loads, f))
