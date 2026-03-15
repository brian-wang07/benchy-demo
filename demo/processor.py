def enrich_transactions(transactions, users):
    """
    Combines transaction data with user data using a hash-map for O(1) lookups.
    """
    # Pre-index users by ID for O(1) lookup.
    # Using reversed(users) ensures that the first occurrence in the original list 
    # is the one that remains in the map, maintaining functional parity with the original 'break' logic.
    user_map = {user['id']: user for user in reversed(users)}
    
    # Use list comprehension for faster iteration and dictionary unpacking for efficient merging
    return [{**txn, 'user': user_map.get(txn['user_id'])} for txn in transactions]

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
