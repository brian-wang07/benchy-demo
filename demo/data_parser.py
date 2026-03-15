import json

@lru_cache(maxsize=128)
def load_transactions(filepath):
    """
    Loads transactions from a JSON file.
    Optimized: Reads into memory and parses in one go, with caching for repeated access.
    """
    with open(filepath, 'r') as f:
        return json.loads(f.read())

@lru_cache(maxsize=128)
def load_users(filepath):
    """
    Loads users from a JSONL file.
    Optimized: Bulk parses the JSONL by converting to a single JSON array for speed.
    """
    with open(filepath, 'r') as f:
        content = f.read().strip()
    if not content:
        return []
    # Convert JSONL to a JSON array: {"a":1}\n{"b":2} -> [{"a":1},{"b":2}]
    return json.loads("[" + content.replace('\n', ',') + "]")
