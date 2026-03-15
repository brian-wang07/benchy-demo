import json

def load_transactions(filepath):
    """
    Loads transactions from a JSON file.
    Optimized: Reads the entire file into memory and parses once.
    """
    with open(filepath, 'r') as f:
        return json.loads(f.read())

def load_users(filepath):
    """
    Loads users from a JSONL file.
    Optimized: Converts JSONL to a single JSON array string to parse in one C call.
    """
    with open(filepath, 'r') as f:
        # Constructing a single JSON array string is faster than N individual loads calls.
        return json.loads(f"[{','.join(f)}]")
