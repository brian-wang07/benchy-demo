def enrich_transactions(transactions, users):
    """
    Combines transaction data with user data.
    Intentional bottleneck: O(N * M) nested loop for lookups.
    """
    # Create a lookup map for users by ID: O(M)
    # We use a loop to ensure we keep the FIRST match found, mimicking the original 'break' logic
    user_map = {}
    for user in users:
        user_id = user['id']
        if user_id not in user_map:
            user_map[user_id] = user

    enriched = []
    for txn in transactions:
        # Dictionary lookup is O(1) on average
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
    # Use a list to collect string fragments for O(N) efficiency
    report_fragments = ["--- TRANSACTION REPORT ---\n"]
    
    for txn in enriched_transactions:
        user_name = txn['user']['name'] if txn['user'] else "Unknown"
        report_fragments.append(f"Transaction ID: {txn['id']} | User: {user_name} | Amount: ${txn['amount']}\n")
        
    report_fragments.append("--- END OF REPORT ---\n")
    return "".join(report_fragments)
