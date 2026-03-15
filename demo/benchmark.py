import asyncio
import aiohttp
import time

async def fetch(session, user_id):
    start = time.time()
    url = f"http://127.0.0.1:8000/user/{user_id}/dashboard"
    try:
        async with session.get(url) as response:
            await response.read()
            return time.time() - start
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return time.time() - start

async def main():
    print("Starting server benchmark with 20 concurrent requests...")
    start_global = time.time()
    
    # Use a TCP connection pool
    connector = aiohttp.TCPConnector(limit=50)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for i in range(20):
            # Hit different random users
            tasks.append(fetch(session, f"user_{i}"))
        
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
