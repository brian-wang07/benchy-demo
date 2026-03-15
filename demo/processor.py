def enrich_transactions(transactions, users):
    """
    Combines transaction data with user data using a hash map for O(1) lookups.
    """
    user_map = {user['id']: user for user in users}
    
    enriched = []
    for txn in transactions:
        # O(1) lookup instead of O(M) scan
        user_info = user_map.get(txn['user_id'])
        
        # Merge dictionaries efficiently
        enriched_txn = {**txn, 'user': user_info}
        enriched.append(enriched_txn)
        
    return enriched

def generate_report(enriched_transactions):
    """
    Generates a textual report of all enriched transactions.
    """
    report = "--- TRANSACTION REPORT ---\n"
    
    for txn in enriched_transactions:
        # Runtime/Memory bottleneck: String immutability causes a new string 
        # allocation and copy on each iteration
        user_name = txn['user']['name'] if txn['user'] else "Unknown"
        report += f"Transaction ID: {txn['id']} | User: {user_name} | Amount: ${txn['amount']}\n"
        
    report += "--- END OF REPORT ---\n"
    return report
