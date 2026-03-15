# Advanced Web Server Bottleneck Demo

This project tests an optimization agent's ability to locate highly nuanced bugs that exist predominantly in web servers contexts, where concurrency, memory leaking, and data-retrieval patterns dictate performance. Unlike simple processing scripts, servers suffer drastically from incorrect event-loop usage and I/O inefficiencies.

## How to Run

1. **Install dependencies:**
   ```bash
   cd advanced_demo
   pip install -r requirements.txt
   ```

2. **Generate the mock database:**
   ```bash
   python data_generator.py
   ```

3. **Start the FastAPI Server:**
   Keep this running in one terminal.
   ```bash
   uvicorn server:app --port 8000
   ```

4. **Run the Benchmark:**
   In a *second* terminal, execute the concurrent load tester.
   ```bash
   python benchmark.py
   ```

## Optimization Opportunities (Agent Targets)

### 1. Concurrency: Blocking the Async Event Loop
* **File:** `server.py`
* **Function:** `user_dashboard()` 
* **Issue:** The endpoint uses `async def` but executes a synchronous blocking call `time.sleep(0.2)` (which simulates a sync DB driver or dense CPU computation). FastAPI runs `async def` endpoints directly on its single async event loop thread. By sleeping synchronously, it prevents the server from processing *any* other requests simultaneously. Max request times will scale linearly with concurrency.
* **Expected Fix:** The agent should either use native asynchronous sleep (`await asyncio.sleep(0.2)`), or drop the `async` keyword to use standard `def` which offloads the handler to FastAPI's background threadpool, thereby unlocking parallel execution.

### 2. File/IO Parsing Churn
* **File:** `database.py`
* **Issue:** `get_user()` and `get_transaction()` both open and parse the entirety of `db.json` on *every single invocation*.
* **Expected Fix:** The agent should cache the parsed JSON payload into memory globally at module startup instead of parsing it per-call. Alternatively, it can memoize the results using `lru_cache`.

### 3. Algorithmic: Relational N+1 Query Execution
* **File:** `server.py`
* **Issue:** The API individually queries `database.get_transaction(tx_id)` inside a `for` loop over the user's transactions array. Paired with bottleneck #2, this yields an immense redundant workload (re-parsing the massive JSON file $N$ times per endpoint hit!).
* **Expected Fix:** The agent should implement a bulk fetch strategy like `database.get_transactions(tx_ids_list)`, looping internally on the DB side without re-opening the payload, or natively yielding a merged structure.

### 4. Memory: Unbounded Global Cache Leaking
* **File:** `server.py`
* **Issue:** The `analytics_data` global dictionary indiscriminately inserts request traces using a highly unique key `f"{request.url}_{time.time()}"`. Since this structure is completely unbounded and never cleaned up, continuous HTTP traffic will permanently inflate the worker process's RAM.
* **Expected Fix:** The agent should recognize the unbound dictionary expansion and suggest an active cap: either using standard `functools.lru_cache`, `cachetools`, an explicitly maxed queue size, or shifting the analytics off-memory entirely.