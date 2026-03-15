import json

DB_FILE = "db.json"

_DB_CACHE = None

def _get_data():
    global _DB_CACHE
    if _DB_CACHE is None:
        with open(DB_FILE, "r") as f:
            _DB_CACHE = json.load(f)
    return _DB_CACHE

def get_user(user_id: str):
    """
    Fetches a user from the cached DB.
    Optimized: Uses a singleton-style cache to avoid repeated disk I/O.
    """
    data = _get_data()
    return data["users"].get(user_id)

def get_transaction(tx_id: str):
    """
    Fetches a transaction from the cached DB.
    Optimized: Uses a singleton-style cache to avoid repeated disk I/O.
    """
    data = _get_data()
    return data["transactions"].get(tx_id)
