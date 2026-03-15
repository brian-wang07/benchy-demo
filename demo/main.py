import time
import concurrent.futures
from data_parser import load_transactions, load_users
from processor import enrich_transactions, generate_report

def main():
    print("Starting processing pipeline...")
    start_time = time.time()
    
    print("Loading users and transactions...")
    users = load_users("users.jsonl")
    txs = load_transactions("transactions.json")
    
    print(f"Enriching {len(txs)} transactions...")
    # Pre-index users by ID to convert O(N*M) scan into O(1) lookup
    user_map = {user['id']: user for user in users}
    for tx in txs:
        # Assuming the logic is to match transaction user_id with user id
        tx['user'] = user_map.get(tx['user_id'])
    enriched = txs
    
    print("Generating report...")
    report = generate_report(enriched)
    
    print("Writing report to disk...")
    with open("final_report.txt", "w") as f:
        f.write(report)
        
    end_time = time.time()
    print(f"Pipeline finished in {end_time - start_time:.4f} seconds.")

if __name__ == "__main__":
    # Ensure you run `python generator.py` first to create the data files.
    main()
