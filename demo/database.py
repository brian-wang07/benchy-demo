import json
import functools

DB_FILE = "db.json"

@functools.lru_cache(maxsize=1)
def _load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def get_user(user_id: str):
    """
    Simulates a DB fetch for a user.
    """
    data = _load_db()
    return data["users"].get(user_id)

def get_transaction(tx_id: str):
    """
    Simulates a DB fetch for a single transaction.
    """
    data = _load_db()
    return data["transactions"].get(tx_id)
