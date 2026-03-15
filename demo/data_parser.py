import json

import json
from functools import lru_cache

@lru_cache(maxsize=None)
def load_transactions(filepath):
    """
    Loads transactions from a JSON file.
    Optimized with caching and binary bulk reading for maximum speed.
    """
    with open(filepath, 'rb') as f:
        return json.loads(f.read())

@lru_cache(maxsize=None)
def load_users(filepath):
    """
    Loads users from a JSONL file.
    Optimized with caching and map() for faster processing.
    """
    with open(filepath, 'rb') as f:
        return list(map(json.loads, f))
