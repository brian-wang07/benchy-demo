import json

def load_transactions(filepath):
    """
    Loads transactions from a JSON file.
    Optimized: Reads the entire file into memory as bytes for faster parsing by json.loads.
    """
    with open(filepath, 'rb') as f:
        return json.loads(f.read())

def load_users(filepath):
    """
    Loads users from a JSONL file.
    Optimized: Reads the file in binary mode and parses as a single JSON array to maximize speed.
    """
    with open(filepath, 'rb') as f:
        content = f.read().strip()
    if not content:
        return []
    # Convert JSONL to a JSON array and parse once for maximum speed
    return json.loads(b'[' + content.replace(b'\\n', b',') + b']')
