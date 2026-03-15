import json

def load_transactions(filepath):
    """
    Loads transactions from a JSON file.
    Optimized: Uses binary read and loads directly for maximum speed.
    """
    with open(filepath, 'rb') as f:
        return json.loads(f.read())

def load_users(filepath):
    """
    Loads users from a JSONL file.
    Optimized: Uses list(map(...)) and binary iteration for faster parsing.
    """
    with open(filepath, 'rb') as f:
        return list(map(json.loads, f))
