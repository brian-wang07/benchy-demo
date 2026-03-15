import json

def load_transactions(filepath):
    """
    Loads transactions from a JSON file.
    Optimized: Uses bulk binary read and loads() for maximum parsing speed.
    """
    with open(filepath, 'rb') as f:
        return json.loads(f.read())

def load_users(filepath):
    """
    Loads users from a JSONL file.
    Optimized: Uses binary mode and map to move iteration and decoding into C.
    """
    with open(filepath, 'rb') as f:
        return list(map(json.loads, f))
