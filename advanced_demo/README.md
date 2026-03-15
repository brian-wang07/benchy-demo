# Advanced Python Bottlenecks Demo

This module demonstrates more nuanced runtime and memory bottlenecks in Python code, particularly when dealing with bulk data processing. The optimizations here require a deeper understanding of Python's internal memory management and standard library overhead.

## How to run
Run the main file to generate the data and get baseline benchmarks:
```bash
cd advanced_demo
python main.py
```

## Optimization Opportunities (Agent Targets)

### 1. Memory Bottleneck: Missing `__slots__`
* **File:** `parser.py` 
* **Class:** `SensorReading`
* **Issue:** By default, Python creates a dynamic `__dict__` dictionary for every object instance. When allocating 500,000 objects in memory, this dictionary overhead becomes enormous, unnecessarily consuming large amounts of RAM.
* **Expected Optimization:** Add `__slots__ = ['timestamp', 'sensor_id', 'temperature', 'status']` to the class definition to prevent `__dict__` creation. This yields a massive reduction in memory usage.

### 2. Memory Bottleneck: Eager List Appends vs. Lazy Generators
* **File:** `analytics.py`
* **Function:** `filter_active_sensors()`
* **Issue:** The function iterates over all readings and appends active ones to a completely new list, duplicating references and taking up a large chunk of memory simultaneously.
* **Expected Optimization:** Change this to a generator structure (using `yield r` or a generator expression) to iterate lazily, achieving a near-zero memory footprint.

### 3. Runtime Bottleneck: Expensive Standard Library Calls inside Loops
* **File:** `analytics.py`
* **Function:** `extract_dates()`
* **Issue:** It uses `datetime.strptime()` within a loop. The overhead of safely parsing and instantiating `datetime` objects repeatedly in Python is notoriously high.
* **Expected Optimization:** Because the timestamp is a strictly formatted, fixed-length ISO8601 string (`YYYY-MM-DDTHH:MM:SSZ`), date extraction can be dramatically accelerated by using standard string slicing (e.g., `r.timestamp[:10]`) instead of instantiating `datetime` objects.

### 4. Runtime / Algorithmic Bottleneck: Repeated Window Operations $O(N \cdot K)$
* **File:** `analytics.py`
* **Function:** `moving_average()`
* **Issue:** It calculates a slice sum `sum(temps[i:i+window])` on every iteration. This performs horribly since it throws away prior work and recalculates the entire window sum every single time.
* **Expected Optimization:** It should maintain a running sum, simply adding the new element and subtracting the oldest element as the window shifts forward. This makes the loop $O(N)$ instead of $O(N \cdot K)$.

### 5. I/O Bottleneck: Synchronous N+1 API Calls
* **File:** `api_client.py`
* **Function:** `get_locations_for_sensors()`
* **Issue:** The function iterates over a list of sensor IDs and makes a synchronous, blocking "network" API call `time.sleep()` for each one. Because it executes sequentially, the program drops the ball while waiting on network latency—causing execution time to scale linearly with array length.
* **Expected Optimization:** The agent should recognize that I/O-bound tasks inside a loop can be aggressively parallelized. It should replace the sequential loop with concurrency (e.g., using `concurrent.futures.ThreadPoolExecutor` or refactoring to `asyncio.gather`), overlapping the latency periods and significantly crushing the runtime.