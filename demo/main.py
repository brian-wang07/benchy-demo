import time
import concurrent.futures
from data_parser import load_transactions, load_users
from processor import enrich_transactions, generate_report

def main():
    print("Starting processing pipeline...")
    start_time = time.time()
    
    print("Loading users and transactions concurrently...")
    # Using ProcessPoolExecutor allows true parallel CPU execution for parsing, bypassing the GIL.
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        future_users = executor.submit(load_users, "users.jsonl")
        future_txs = executor.submit(load_transactions, "transactions.json")
        users = future_users.result()
        txs = future_txs.result()
    
    print(f"Enriching {len(txs)} transactions with {len(users)} users...")
    enriched = enrich_transactions(txs, users)
    
    # Crucial: Free up the large raw data lists as soon as enrichment is done 
    # to lower peak memory before generating the final report string.
    del txs
    del users
    
    print("Generating report...")
    report = generate_report(enriched)
    del enriched
    
    print("Writing report to disk...")
    with open("final_report.txt", "w") as f:
        f.write(report)
        
    end_time = time.time()
    print(f"Pipeline finished in {end_time - start_time:.4f} seconds.")

if __name__ == "__main__":
    # Ensure you run `python generator.py` first to create the data files.
    main()
