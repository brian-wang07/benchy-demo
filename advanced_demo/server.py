from fastapi import FastAPI, Request, HTTPException
import time
import database

app = FastAPI()

# Global dictionary used as a naive analytics cache
# Bottleneck #4: Unbounded memory leak
analytics_data = {}

import asyncio
from fastapi.concurrency import run_in_threadpool

@app.get("/user/{user_id}/dashboard")
async def user_dashboard(user_id: str, request: Request):
    """
    Endpoint mapping a user's dashboard.
    """
    
    # Fix Bottleneck #1: Non-blocking sleep allows the event loop to handle other requests.
    await asyncio.sleep(0.2) 
    
    # Fix Bottleneck #2: Offload blocking sync I/O to a threadpool to keep the loop free.
    user = await run_in_threadpool(database.get_user, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Fix Bottleneck #3: Solve N+1 by fetching all transactions in parallel.
    # Instead of N sequential calls, we execute them concurrently in the thread pool.
    tx_ids = user.get("transactions", [])
    if tx_ids:
        tasks = [run_in_threadpool(database.get_transaction, tx_id) for tx_id in tx_ids]
        # Gather all results concurrently
        results = await asyncio.gather(*tasks)
        enriched_txs = [tx for tx in results if tx]
    else:
        enriched_txs = []
            
    response = {
        "user_info": user["name"],
        "transaction_count": len(enriched_txs),
        "transactions": enriched_txs
    }
    
    # Fix Bottleneck #4: Prevent unbounded memory leak with a FIFO eviction strategy.
    # Dicts in Python 3.7+ maintain insertion order, making this O(1).
    if len(analytics_data) >= 10000:
        analytics_data.pop(next(iter(analytics_data)))

    unique_request_id = f"{request.url}_{time.time()}"
    analytics_data[unique_request_id] = {
        "user_id": user_id,
        "tx_count": len(enriched_txs)
    }
    
    return response
