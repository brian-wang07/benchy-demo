def enrich_transactions(transactions, users):
    """
    Combines transaction data with user data.
    """
    user_lookup = {user['id']: user for user in users}
    enriched = []
    for txn in transactions:
        enriched_txn = txn.copy()
        enriched_txn['user'] = user_lookup.get(txn['user_id'])
        enriched.append(enriched_txn)
        
    return enriched

def generate_report(enriched_transactions):
    """
    Generates a textual report of all enriched transactions.
    """
    def report_generator():
        yield "--- TRANSACTION REPORT ---\n"
        for txn in enriched_transactions:
            user_name = txn['user']['name'] if txn['user'] else "Unknown"
            yield f"Transaction ID: {txn['id']} | User: {user_name} | Amount: ${txn['amount']}\n"
        yield "--- END OF REPORT ---\n"
        
    return "".join(report_generator())
