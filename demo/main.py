import time
import concurrent.futures
from data_parser import load_transactions, load_users
from processor import enrich_transactions, generate_report

def main():
    print("Starting processing pipeline...")
    # Use perf_counter for more accurate high-performance timing
    start_time = time.perf_counter()
    
    print("Loading users and transactions concurrently...")
    # Parallel loading is kept to maximize I/O throughput and overlap CPU-bound parsing
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_users = executor.submit(load_users, "users.jsonl")
        future_txs = executor.submit(load_transactions, "transactions.json")
        users = future_users.result()
        txs = future_txs.result()
    
    # Enrichment Phase
    print(f"Enriching {len(txs)} transactions with {len(users)} users...")
    enriched = enrich_transactions(txs, users)
    
    # MEMORY OPTIMIZATION: Immediately release references to raw input datasets.
    # This prevents the program from holding users, txs, AND enriched in memory at once.
    del users
    del txs
    
    print("Generating report...")
    report = generate_report(enriched)
    
    # MEMORY OPTIMIZATION: Release enriched data before disk I/O
    del enriched
    
    print("Writing report to disk...")
    with open("final_report.txt", "w") as f:
        f.write(report)
    
    # Final cleanup
    del report
        
    end_time = time.perf_counter()
    print(f"Pipeline finished in {end_time - start_time:.4f} seconds.")

if __name__ == "__main__":
    # Ensure you run `python generator.py` first to create the data files.
    main()
