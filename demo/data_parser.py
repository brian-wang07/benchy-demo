import json

def load_transactions(filepath):
    """
    Loads transactions from a JSON file.
    Optimized: Uses bulk read and fast string decoding for maximum throughput.
    """
    with open(filepath, 'r') as f:
        return json.loads(f.read())

def load_users(filepath):
    """
    Loads users from a JSONL file.
    Intentional bottleneck: Uses readlines() which loads all lines into memory.
    """
    with open(filepath, 'r') as f:
        users = [json.loads(line) for line in f]
    return users
