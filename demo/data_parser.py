import json

def load_transactions(filepath):
    """
    Loads transactions from a JSON file.
    Optimized by reading in binary mode to skip Python-level text decoding.
    """
    with open(filepath, 'rb') as f:
        return json.loads(f.read())

def load_users(filepath):
    """
    Loads users from a JSONL file.
    Optimized by joining all lines into a single JSON array and parsing once.
    """
    with open(filepath, 'rb') as f:
        return json.loads(b'[' + b','.join(f) + b']')
