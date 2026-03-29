import json

def load_transactions(filepath):
    """
    Loads transactions from a JSON file.
    Optimized: Reading into memory first then parsing is faster for the standard json library.
    """
    with open(filepath, 'r') as f:
        return json.loads(f.read())

def load_users(filepath):
    """
    Loads users from a JSONL file.
    Optimized: Wrap lines into a single JSON array to use the faster C parser pass.
    """
    with open(filepath, 'r') as f:
        # Joining lines into a single string and parsing once is faster than line-by-line parsing
        return json.loads(f\"[{','.join(f)}]\")
