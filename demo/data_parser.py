import json

def load_transactions(filepath):
    """
    Loads transactions from a JSON file.
    Optimized: Reads the entire file into memory first to speed up parsing.
    """
    with open(filepath, 'r') as f:
        return json.loads(f.read())

def load_users(filepath):
    """
    Loads users from a JSONL file.
    Optimized: Uses f.read().splitlines() and map() to minimize Python loop overhead.
    """
    with open(filepath, 'r') as f:
        return list(map(json.loads, f.read().splitlines()))
