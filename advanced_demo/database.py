import json

DB_FILE = "db.json"

_db_cache = None

def _get_db():
    global _db_cache
    if _db_cache is None:
        with open(DB_FILE, "r") as f:
            _db_cache = json.load(f)
    return _db_cache

def get_user(user_id: str):
    """
    Simulates a DB fetch for a user.
    Optimized: Uses a module-level cache to avoid redundant I/O and JSON parsing.
    """
    return _get_db()[\"users\"].get(user_id)

def get_transaction(tx_id: str):
    """
    Simulates a DB fetch for a single transaction.
    Optimized: Uses a module-level cache to avoid redundant I/O and JSON parsing.
    """
    return _get_db()[\"transactions\"].get(tx_id)
