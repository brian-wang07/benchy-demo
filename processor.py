def enrich_transactions(transactions, users):
    """
    Combines transaction data with user data.
    Intentional bottleneck: O(N * M) nested loop for lookups.
    """
    # Optimized: Create a hash map for O(1) user lookups
    user_lookup = {user['id']: user for user in users}
    
    return [
        {**txn, 'user': user_lookup.get(txn['user_id'])}
        for txn in transactions
    ]

def generate_report(enriched_transactions):
    """
    Generates a textual report of all enriched transactions.
    Intentional bottleneck: Inefficient string concatenation in a loop.
    """
    body = "".join(
        f"Transaction ID: {txn['id']} | User: {txn['user']['name'] if txn['user'] else 'Unknown'} | Amount: ${txn['amount']}\n"
        for txn in enriched_transactions
    )
    
    return f"--- TRANSACTION REPORT ---\n{body}--- END OF REPORT ---\n"
