def enrich_transactions(transactions, users):
    """
    Combines transaction data with user data.
    """
    # Create a lookup map for users. O(U) time complexity.
    # We manually build the dict to ensure parity with the original 'break' logic 
    # (keeping the first occurrence of a user ID).
    user_map = {}
    for user in users:
        u_id = user['id']
        if u_id not in user_map:
            user_map[u_id] = user
    
    # Enrich transactions using the map. O(T) time complexity.
    # Total complexity: O(T + U)
    return [{**txn, 'user': user_map.get(txn['user_id'])} for txn in transactions]

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
