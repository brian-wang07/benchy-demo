import json

DB_FILE = "db.json"

_USERS_CACHE = None
_TX_CACHE = None

def _initialize_cache():
    global _USERS_CACHE, _TX_CACHE
    with open(DB_FILE, "r") as f:
        data = json.load(f)
    # Storing sub-dictionaries directly for O(1) access
    _USERS_CACHE = data["users"]
    _TX_CACHE = data["transactions"]

def get_user(user_id: str):
    """
    Simulates a DB fetch for a user.
    Optimized: Uses a cache to avoid repeated file I/O and JSON parsing.
    """
    if _USERS_CACHE is None:
        _initialize_cache()
    return _USERS_CACHE.get(user_id)

def get_transaction(tx_id: str):
    """
    Simulates a DB fetch for a single transaction.
    Optimized: Uses a cache to avoid repeated file I/O and JSON parsing.
    """
    if _TX_CACHE is None:
        _initialize_cache()
    return _TX_CACHE.get(tx_id)
