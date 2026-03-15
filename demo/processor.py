def enrich_transactions(transactions, users):
    """
    Combines transaction data with user data.
    """
    # O(U) pre-indexing: use reversed to ensure first-hit parity for duplicate IDs
    user_lookup = {u['id']: u for u in reversed(users)}
    
    # O(T) processing via list comprehension and dict merging
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
