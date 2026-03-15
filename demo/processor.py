def enrich_transactions(transactions, users):
    """
    Combines transaction data with user data.
    """
    user_lookup = {user['id']: user for user in users}
    return [
        {**txn, 'user': user_lookup.get(txn['user_id'])}
        for txn in transactions
    ]

def generate_report(enriched_transactions):
    """
    Generates a textual report of all enriched transactions.
    """
    return (
        "--- TRANSACTION REPORT ---\n" +
        "".join(
            f"Transaction ID: {txn['id']} | User: {txn['user']['name'] if txn['user'] else 'Unknown'} | Amount: ${txn['amount']}\n"
            for txn in enriched_transactions
        ) +
        "--- END OF REPORT ---\n"
    )
