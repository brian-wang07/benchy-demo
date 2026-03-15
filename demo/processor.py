def enrich_transactions(transactions, users):
    """
    Combines transaction data with user data.
    """
    user_lookup = {user['id']: user for user in users}
    enriched = []
    for txn in transactions:
        # Merge dictionaries
        enriched_txn = txn.copy()
        enriched_txn['user'] = user_lookup.get(txn['user_id'])
        enriched.append(enriched_txn)
        
    return enriched

def generate_report(enriched_transactions):
    """
    Generates a textual report of all enriched transactions.
    """
    parts = ["--- TRANSACTION REPORT ---\n"]
    
    for txn in enriched_transactions:
        # Collect parts in a list to avoid string reallocation
        user_name = txn['user']['name'] if txn['user'] else "Unknown"
        parts.append(f"Transaction ID: {txn['id']} | User: {user_name} | Amount: ${txn['amount']}\n")
        
    parts.append("--- END OF REPORT ---\n")
    return "".join(parts)
