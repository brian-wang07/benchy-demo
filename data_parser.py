import json

def load_transactions(filepath):
    """
    Loads transactions from a JSON file.
    Intentional bottleneck: Reads the entire file into a giant string first.
    """
    with open(filepath, 'r') as f:
        return json.load(f)

def load_users(filepath):
    """
    Loads users from a JSONL file.
    Intentional bottleneck: Uses readlines() which loads all lines into memory.
    """
    with open(filepath, 'r') as f:
        return [json.loads(line) for line in f]
