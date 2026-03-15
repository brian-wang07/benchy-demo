def enrich_transactions(transactions, users):
    """
    Combines transaction data with user data using O(1) lookups.
    """
    # Pre-compute a user lookup table for O(1) access
    user_map = {user['id']: user for user in users}
    
    enriched = []
    for txn in transactions:
        # Dictionary lookup is significantly faster than a nested loop
        user_info = user_map.get(txn['user_id'])
        
        # Create a copy and add the user info to maintain functional parity
        enriched_txn = txn.copy()
        enriched_txn['user'] = user_info
        enriched.append(enriched_txn)
        
    return enriched

def generate_report(enriched_transactions):
    """
    Generates a textual report using efficient string joining.
    """
    lines = ["--- TRANSACTION REPORT ---\n"]
    
    for txn in enriched_transactions:
        # Get user name with fallback, same logic as original
        user_name = txn['user']['name'] if txn['user'] else "Unknown"
        # Append to list instead of concatenating strings
        lines.append(f"Transaction ID: {txn['id']} | User: {user_name} | Amount: ${txn['amount']}\n")
        
    lines.append("--- END OF REPORT ---\n")
    # Join all segments in a single O(L) operation
    return "".join(lines)
