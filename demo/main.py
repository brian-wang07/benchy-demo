import time
import concurrent.futures
from data_parser import load_transactions, load_users
from processor import enrich_transactions, generate_report

def main():
    print("Starting processing pipeline...")
    # Use perf_counter for more accurate timing measurements
    start_time = time.perf_counter()
    
    print("Loading users and transactions concurrently...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_users = executor.submit(load_users, "users.jsonl")
        future_txs = executor.submit(load_transactions, "transactions.json")
        users = future_users.result()
        txs = future_txs.result()
    
    # Free future objects which hold references to the loaded data
    del future_users, future_txs
    
    print(f"Enriching {len(txs)} transactions with {len(users)} users...")
    enriched = enrich_transactions(txs, users)
    
    # Optimization: Clear raw data references immediately after enrichment
    # to reduce peak memory usage while generating the report.
    del txs, users
    
    print("Generating report...")
    report = generate_report(enriched)
    
    # Optimization: Clear enriched data reference before the I/O-heavy write
    del enriched
    
    print("Writing report to disk...")
    with open("final_report.txt", "w") as f:
        f.write(report)
        
    # Final cleanup of the report string
    del report
        
    end_time = time.perf_counter()
    print(f"Pipeline finished in {end_time - start_time:.4f} seconds.")

if __name__ == "__main__":
    # Ensure you run `python generator.py` first to create the data files.
    main()
