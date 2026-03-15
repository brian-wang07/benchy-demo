import json

DB_FILE = "db.json"

from functools import lru_cache

@lru_cache(maxsize=1)
def _load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def get_user(user_id: str):
    """
    Simulates a DB fetch for a user.
    Bottleneck: Opens and decodes the entire JSON payload on every single call.
    """
    data = _load_db()
    return data["users"].get(user_id)

def get_transaction(tx_id: str):
    """
    Simulates a DB fetch for a single transaction.
    Bottleneck: Also opens and decodes the JSON payload for *every* individual transaction.
    """
    data = _load_db()
    return data["transactions"].get(tx_id)
