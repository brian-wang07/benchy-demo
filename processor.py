def enrich_transactions(transactions, users):
    """
    Combines transaction data with user data.
    Intentional bottleneck: O(N * M) nested loop for lookups.
    """
    user_dict = {}
    for user in users:
        if user['id'] not in user_dict:
            user_dict[user['id']] = user

    return [{**txn, 'user': user_dict.get(txn['user_id'])} for txn in transactions]

def generate_report(enriched_transactions):
    """
    Generates a textual report of all enriched transactions.
    Intentional bottleneck: Inefficient string concatenation in a loop.
    """
    report_lines = [
        f"Transaction ID: {txn['id']} | User: {txn['user']['name'] if txn['user'] else 'Unknown'} | Amount: ${txn['amount']}\n"
        for txn in enriched_transactions
    ]
    
    return "".join([
        "--- TRANSACTION REPORT ---\n",
        *report_lines,
        "--- END OF REPORT ---\n"
    ])
