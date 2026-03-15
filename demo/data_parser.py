import json

@functools.lru_cache(maxsize=None)
def load_transactions(filepath):
    """
    Loads transactions from a JSON file.
    Optimized: Uses lru_cache for O(1) repeated access and faster string-based parsing.
    """
    with open(filepath, 'r') as f:
        return json.loads(f.read())

@functools.lru_cache(maxsize=None)
def load_users(filepath):
    """
    Loads users from a JSONL file.
    Optimized: Uses a single bulk parse via string join for maximum speed.
    """
    with open(filepath, 'r') as f:
        return json.loads(f\"[{','.join(f)}]\")
