def enrich_transactions(transactions, users):
    """
    Combines transaction data with user data.
    Intentional bottleneck: O(N * M) nested loop for lookups.
    """
    enriched = []
    for txn in transactions:
        user_info = None
        # Runtime bottleneck: Iterating through the entire users list for every transaction
        for user in users:
            if user['id'] == txn['user_id']:
                user_info = user
                break
        
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
