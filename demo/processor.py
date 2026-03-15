def enrich_transactions(transactions, users):
    """
    Combines transaction data with user data using a lookup table for O(1) matching.
    """
    user_map = {user['id']: user for user in users}
    get_user = user_map.get
    
    # List comprehension is faster than manual loops with .append()
    # dict(txn, user=...) is an efficient way to create a shallow copy with updates
    return [dict(txn, user=get_user(txn['user_id'])) for txn in transactions]

def generate_report(enriched_transactions):
    """
    Generates a textual report using list joining for efficient string building.
    """
    # Use a list to collect parts for O(N) efficiency
    parts = ["--- TRANSACTION REPORT ---"]
    
    for txn in enriched_transactions:
        user_name = txn['user']['name'] if txn['user'] else "Unknown"
        parts.append(f"Transaction ID: {txn['id']} | User: {user_name} | Amount: ${txn['amount']}")
        
    parts.append("--- END OF REPORT ---")
    
    # Joining with newline and adding a trailing newline to match original output exactly
    return "\n".join(parts) + "\n"
