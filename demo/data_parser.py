import json

def load_transactions(filepath):
    """
    Loads transactions from a JSON file.
    Optimized: Opens in binary mode to bypass Python-level text decoding.
    """
    with open(filepath, 'rb') as f:
        data = json.loads(f.read())
    return data

def load_users(filepath):
    """
    Loads users from a JSONL file.
    Optimized: Uses binary mode and map() for faster parsing and reduced overhead.
    """
    with open(filepath, 'rb') as f:
        users = list(map(json.loads, f))
    return users
