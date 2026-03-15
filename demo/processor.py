def enrich_transactions(transactions, users):
    """
    Combines transaction data with user data.
    """
    # Pre-compute a user lookup table for O(1) access
    user_map = {user['id']: user for user in users}
    
    enriched = []
    for txn in transactions:
        user_info = user_map.get(txn['user_id'])
        
        # Merge dictionaries
        enriched_txn = txn.copy()
        enriched_txn['user'] = user_info
        enriched.append(enriched_txn)
        
    return enriched

def generate_report(enriched_transactions):
    """
    Generates a textual report of all enriched transactions.
    """
    # Use a list to collect string segments to avoid O(N^2) string concatenation
    lines = ["--- TRANSACTION REPORT ---\n"]
    
    for txn in enriched_transactions:
        user_name = txn['user']['name'] if txn['user'] else "Unknown"
        lines.append(f"Transaction ID: {txn['id']} | User: {user_name} | Amount: ${txn['amount']}\n")
        
    lines.append("--- END OF REPORT ---\n")
    return "".join(lines)
