import asyncio
import aiohttp
import time

async def fetch(session, user_id):
    url = f"http://127.0.0.1:8000/user/{user_id}/dashboard"
    start = time.perf_counter()
    try:
        async with session.get(url) as response:
            await response.json()
        return time.perf_counter() - start
    except Exception as e:
        # Capture latency immediately to avoid including logging overhead
        elapsed = time.perf_counter() - start
        # Offload the blocking print without awaiting it to keep the task lifecycle short
        loop = asyncio.get_running_loop()
        loop.run_in_executor(None, print, f"Error fetching {url}: {e}")
        return elapsed

async def main():
    print("Starting server benchmark with 20 concurrent requests...")
    start_global = time.time()
    
    # Use a TCP connection pool
    connector = aiohttp.TCPConnector(limit=50)
    async with aiohttp.ClientSession(connector=connector) as session:
        # Optimization: Use list comprehension for faster task creation
        tasks = [fetch(session, f"user_{i}") for i in range(20)]
        times = await asyncio.gather(*tasks)
    
    end_global = time.time()
    print("--------------------------------------------------")
    print(f"Benchmark finished in {end_global - start_global:.2f} seconds.")
    print(f"Average request latency: {sum(times)/len(times):.2f} seconds.")
    print(f"Max request latency:     {max(times):.2f} seconds.")
    print("--------------------------------------------------")
    
    if max(times) > 4.0:
        print("RESULT: Severe bottlenecks detected! Max latency is very high.")
    else:
        print("RESULT: Performance looks optimal!")

if __name__ == "__main__":
    asyncio.run(main())
