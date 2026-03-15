def enrich_transactions(transactions, users):
    """
    Combines transaction data with user data.
    Optimized: O(N + M) using a hash map for user lookups.
    """
    # Build a lookup table for users. 
    # We only set the key if it's not present to match the 'break' behavior (first match wins).
    user_map = {}
    for user in users:
        u_id = user['id']
        if u_id not in user_map:
            user_map[u_id] = user
            
    enriched = []
    for txn in transactions:
        # O(1) average case lookup
        user_info = user_map.get(txn['user_id'])
        
        # Merge dictionaries
        enriched_txn = txn.copy()
        enriched_txn['user'] = user_info
        enriched.append(enriched_txn)
        
    return enriched

def generate_report(enriched_transactions):
    """
    Generates a textual report of all enriched transactions.
    Intentional bottleneck: Inefficient string concatenation in a loop.
    """
    report = "--- TRANSACTION REPORT ---\n"
    
    for txn in enriched_transactions:
        # Runtime/Memory bottleneck: String immutability causes a new string 
        # allocation and copy on each iteration
        user_name = txn['user']['name'] if txn['user'] else "Unknown"
        report += f"Transaction ID: {txn['id']} | User: {user_name} | Amount: ${txn['amount']}\n"
        
    report += "--- END OF REPORT ---\n"
    return report
