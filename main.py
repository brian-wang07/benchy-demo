import time
from data_parser import load_transactions, load_users
from processor import enrich_transactions, generate_report

def main():
    print("Starting processing pipeline...")
    start_time = time.time()
    
    print("Loading users...")
    users = load_users("users.jsonl")
    
    print("Loading transactions...")
    txs = load_transactions("transactions.json")
    
    print(f"Enriching {len(txs)} transactions with {len(users)} users...")
    enriched = enrich_transactions(txs, users)
    
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
