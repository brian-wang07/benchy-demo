import json

def load_transactions(filepath):
    """
    Loads transactions from a JSON file.
    Optimized: Reads the entire file into memory first to leverage the faster string-based C parser.
    """
    with open(filepath, 'r') as f:
        return json.loads(f.read())

def load_users(filepath):
    """
    Loads users from a JSONL file.
    Optimized: Uses map() for a faster C-based iteration loop over the file lines.
    """
    with open(filepath, 'r') as f:
        return list(map(json.loads, f))
