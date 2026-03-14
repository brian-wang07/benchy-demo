# Code Optimization Agent Benchmark

This repository serves as a benchmark for testing the functionality, effectiveness, and speed of automated code optimization agents. 

The project represents a common data processing pipeline that reads JSON and JSON Lines (JSONL) files, merges the datasets, and generates a formatted textual report. The code is fully functional but contains intentionally introduced, classic performance bottlenecks that scale poorly with dataset size. 

An effective optimization agent should be able to parse this multi-file project, identify the bottlenecks, and implement memory and runtime optimizations without altering the program's observable output.

## How to Run

1. **Generate the Mock Data:**
   Run the generator script to create the necessary dataset (`users.jsonl` and `transactions.json`).
   ```bash
   python generator.py
   ```

2. **Run the Pipeline (Baseline):**
   Execute the main script to run the unoptimized data processing pipeline. This will output the execution time and a `final_report.txt` file.
   ```bash
   python main.py
   ```

## Optimization Opportunities (Agent Targets)

The following bottlenecks have been intentionally designed into the codebase for the agent to find and fix.

### 1. Runtime / Algorithmic Bottleneck (Cross-file Dependency)
* **File:** `processor.py`
* **Function:** `enrich_transactions()`
* **Issue:** The script matches transactions to users using a nested `for` loop, resulting in $O(N \times M)$ elapsed time, where $N$ is the number of transactions and $M$ is the number of users.
* **Expected Optimization:** The agent should convert the `users` list into a hash map/dictionary mapping `user_id -> user` before iterating over transactions. This reduces the time complexity to $O(N + M)$ and provides significant runtime savings.

### 2. Memory Bottleneck (Inefficient File Parsing)
* **File:** `data_parser.py`
* **Functions:** `load_users()` and `load_transactions()`
* **Issue:** In `load_users()`, the code calls `f.readlines()`, which reads the entire file into memory as a massive list of strings before iterating. In `load_transactions()`, `f.read()` loads the entire file byte string into memory before passing it to `json.loads()`.
* **Expected Optimization:** The agent should stream the JSONL file efficiently by iterating directly over the file object (`for line in f:`), which processes the file line-by-line without hitting memory limits. It should also use `json.load(f)` instead of `json.loads(f.read())` to parse the JSON file directly from the file descriptor.

### 3. String Concatenation Issue (Memory & Runtime)
* **File:** `processor.py`
* **Function:** `generate_report()`
* **Issue:** The report generation uses the `+=` operator inside a large `for` loop. Because Python strings are immutable, this operation continuously allocates and copies increasingly large chunks of memory on every iteration.
* **Expected Optimization:** The agent should gather the string lines into a standard Python list (`lines.append(...)`) inside the loop, and use `"".join(lines)` outside the loop at the end to assemble the final string efficiently.