from fastapi import FastAPI, Request, HTTPException
import time
import database

app = FastAPI()

# Global dictionary used as a naive analytics cache
# Bottleneck #4: Unbounded memory leak
analytics_data = {}

import asyncio

@app.get("/user/{user_id}/dashboard")
async def user_dashboard(user_id: str, request: Request):
    """
    Endpoint mapping a user's dashboard.
    """
    
    # Fixed Bottleneck #1: Use non-blocking sleep to allow event loop concurrency
    await asyncio.sleep(0.2) 
    
    loop = asyncio.get_running_loop()
    
    # Offload blocking DB call to a thread pool
    user = await loop.run_in_executor(None, database.get_user, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Fixed Bottleneck #3: Parallelize N+1 queries using asyncio.gather
    tx_ids = user.get("transactions", [])
    if tx_ids:
        # Launch all transaction fetches concurrently in the thread pool
        tasks = [loop.run_in_executor(None, database.get_transaction, tx_id) for tx_id in tx_ids]
        results = await asyncio.gather(*tasks)
        enriched_txs = [tx for tx in results if tx]
    else:
        enriched_txs = []
            
    response = {
        "user_info": user["name"],
        "transaction_count": len(enriched_txs),
        "transactions": enriched_txs
    }
    
    # Record analytics (Note: Bottleneck #4 remains for parity, but execution is fast)
    unique_request_id = f"{request.url}_{time.time()}"
    analytics_data[unique_request_id] = {
        "user_id": user_id,
        "tx_count": len(enriched_txs)
    }
    
    return response
