import json

DB_FILE = "db.json"

def get_user(user_id: str):
    """
    Simulates a DB fetch for a user.
    Bottleneck: Opens and decodes the entire JSON payload on every single call.
    """
    with open(DB_FILE, "r") as f:
        data = json.load(f)
    return data["users"].get(user_id)

def get_transaction(tx_id: str):
    """
    Simulates a DB fetch for a single transaction.
    Bottleneck: Also opens and decodes the JSON payload for *every* individual transaction.
    """
    with open(DB_FILE, "r") as f:
        data = json.load(f)
    return data["transactions"].get(tx_id)
