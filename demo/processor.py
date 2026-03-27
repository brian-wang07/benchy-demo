def enrich_transactions(transactions, users):
    """
    Combines transaction data with user data.
    """
    user_lookup = {user['id']: user for user in users}
    enriched = []
    for txn in transactions:
        # Use O(1) dictionary lookup instead of O(M) linear scan
        user_info = user_lookup.get(txn['user_id'])
        
        # Merge dictionaries
        enriched_txn = txn.copy()
        enriched_txn['user'] = user_info
        enriched.append(enriched_txn)
        
    return enriched

def generate_report(enriched_transactions):
    """
    Generates a textual report of all enriched transactions.
    """
    fragments = ["--- TRANSACTION REPORT ---\n"]
    
    for txn in enriched_transactions:
        user_name = txn['user']['name'] if txn['user'] else "Unknown"
        fragments.append(f"Transaction ID: {txn['id']} | User: {user_name} | Amount: ${txn['amount']}\n")
        
    fragments.append("--- END OF REPORT ---\n")
    return "".join(fragments)
