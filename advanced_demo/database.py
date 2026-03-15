import json

DB_FILE = "db.json"

_DB_CACHE = None

def _get_db():
    global _DB_CACHE
    if _DB_CACHE is None:
        with open(DB_FILE, "r") as f:
            _DB_CACHE = json.load(f)
    return _DB_CACHE

def get_user(user_id: str):
    """
    Simulates a DB fetch for a user.
    Optimized: Uses a global cache to avoid repeated I/O and JSON parsing.
    """
    data = _get_db()
    return data["users"].get(user_id)

def get_transaction(tx_id: str):
    """
    Simulates a DB fetch for a single transaction.
    Optimized: Uses a global cache to avoid repeated I/O and JSON parsing.
    """
    data = _get_db()
    return data["transactions"].get(tx_id)
