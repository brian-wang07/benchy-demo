def enrich_transactions(transactions, users):
    """
    Combines transaction data with user data.
    """
    user_lookup = {}
    for user in users:
        u_id = user['id']
        if u_id not in user_lookup:
            user_lookup[u_id] = user

    return [{**txn, 'user': user_lookup.get(txn['user_id'])} for txn in transactions]

def generate_report(enriched_transactions):
    """
    Generates a textual report of all enriched transactions.
    """
    lines = ["--- TRANSACTION REPORT ---\n"]
    
    for txn in enriched_transactions:
        user_name = txn['user']['name'] if txn['user'] else "Unknown"
        lines.append(f"Transaction ID: {txn['id']} | User: {user_name} | Amount: ${txn['amount']}\n")
        
    lines.append("--- END OF REPORT ---\n")
    return "".join(lines)
