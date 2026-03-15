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
    Optimized: Uses an in-memory cache to avoid redundant Disk I/O and JSON parsing.
    """
    return _get_db()["users"].get(user_id)

def get_transaction(tx_id: str):
    """
    Simulates a DB fetch for a single transaction.
    Optimized: Uses an in-memory cache to avoid redundant Disk I/O and JSON parsing.
    """
    return _get_db()["transactions"].get(tx_id)
