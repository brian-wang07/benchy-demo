import json

import json
from functools import lru_cache

@lru_cache(maxsize=None)
def load_transactions(filepath):
    """
    Loads transactions from a JSON file.
    Optimized: Uses lru_cache for O(1) repeated access and reads the file into memory 
    at once for faster parsing.
    """
    with open(filepath, 'r') as f:
        return json.loads(f.read())

@lru_cache(maxsize=None)
def load_users(filepath):
    """
    Loads users from a JSONL file.
    Optimized: Uses lru_cache for O(1) repeated access and map() for faster 
    C-level iteration over lines.
    """
    with open(filepath, 'r') as f:
        return list(map(json.loads, f))
