def enrich_transactions(transactions, users):
    """
    Combines transaction data with user data using a lookup table for O(1) access.
    """
    # Pre-process users into a dictionary for O(1) lookups
    user_map = {user['id']: user for user in users}
    
    # Use list comprehension for faster iteration and construction
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
