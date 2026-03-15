def enrich_transactions(transactions, users):
    """
    Combines transaction data with user data using a hash-map lookup for O(1) access.
    """
    # Create a lookup table for users to avoid the nested loop.
    # Note: If duplicate IDs exist, this takes the last one to match standard dict comp speed.
    # If the first occurrence is required, a loop with 'if id not in' check should be used.
    user_lookup = {u['id']: u for u in users}
    
    # Use list comprehension and dictionary unpacking for faster execution.
    return [{**txn, 'user': user_lookup.get(txn['user_id'])} for txn in transactions]

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
