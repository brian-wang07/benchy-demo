def enrich_transactions(transactions, users):
    """
    Combines transaction data with user data using a hash map lookup.
    Optimized: O(N + M) complexity.
    """
    # Index users by id for O(1) lookup
    user_map = {user['id']: user for user in users}
    
    enriched = []
    for txn in transactions:
        # Dictionary lookup is significantly faster than linear search
        user_info = user_map.get(txn['user_id'])
        
        # Merge dictionaries
        enriched_txn = txn.copy()
        enriched_txn['user'] = user_info
        enriched.append(enriched_txn)
        
    return enriched

def generate_report(enriched_transactions):
    """
    Generates a textual report using efficient list joining.
    Optimized: O(N) complexity by avoiding string immutability overhead.
    """
    lines = ["--- TRANSACTION REPORT ---\n"]
    
    for txn in enriched_transactions:
        user_name = txn['user']['name'] if txn['user'] else "Unknown"
        lines.append(f"Transaction ID: {txn['id']} | User: {user_name} | Amount: ${txn['amount']}\n")
        
    lines.append("--- END OF REPORT ---\n")
    return "".join(lines)
