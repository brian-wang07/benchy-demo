import json

def load_transactions(filepath):
    """
    Loads transactions from a JSON file.
    Optimized: Uses binary read and loads() for maximum parsing speed.
    """
    with open(filepath, 'rb') as f:
        return json.loads(f.read())

def load_users(filepath):
    """
    Loads users from a JSONL file.
    Optimized: Uses map() and binary buffer splitting for maximum throughput.
    """
    with open(filepath, 'rb') as f:
        return list(map(json.loads, f.read().splitlines()))
