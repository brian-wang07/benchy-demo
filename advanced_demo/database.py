import json

DB_FILE = "db.json"

_DB_CACHE = None

def _get_db():
    global _DB_CACHE
    if _DB_CACHE is None:
        with open(DB_FILE, "r") as f:
            _DB_CACHE = json.load(f)
    return _DB_CACHE

_USERS_CACHE = None
_TX_CACHE = None

def _initialize_caches():
    global _USERS_CACHE, _TX_CACHE
    with open(DB_FILE, "r") as f:
        # bulk read + loads is often faster than stream parsing for medium-sized JSON
        data = json.loads(f.read())
    _USERS_CACHE = data["users"]
    _TX_CACHE = data["transactions"]

def get_user(user_id: str):
    if _USERS_CACHE is None:
        _initialize_caches()
    return _USERS_CACHE.get(user_id)

def get_transaction(tx_id: str):
    if _TX_CACHE is None:
        _initialize_caches()
    return _TX_CACHE.get(tx_id)
