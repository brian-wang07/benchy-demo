from fastapi import FastAPI, Request, HTTPException
import time
import database

app = FastAPI()

# Global dictionary used as a naive analytics cache
# Bottleneck #4: Unbounded memory leak
analytics_data = {}

import asyncio

# Limit the size of analytics_data to prevent memory leak (Bottleneck #4)
MAX_ANALYTICS_ENTRIES = 10000

@app.get("/user/{user_id}/dashboard")
async def user_dashboard(user_id: str, request: Request):
    """
    Endpoint mapping a user's dashboard.
    """
    
    # Bottleneck #1: Fixed blocking the Async Event Loop
    # Use await asyncio.sleep to allow the event loop to handle other requests.
    await asyncio.sleep(0.2) 
    
    # Offload blocking DB call to a thread to avoid stalling the event loop.
    user = await asyncio.to_thread(database.get_user, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Bottleneck #3: Fixed N+1 Query Anti-Pattern
    # Run transaction lookups in parallel using threads and asyncio.gather.
    tx_ids = user.get("transactions", [])
    tx_tasks = [asyncio.to_thread(database.get_transaction, tx_id) for tx_id in tx_ids]
    results = await asyncio.gather(*tx_tasks)
    
    # Filter out None results to maintain functional parity
    enriched_txs = [tx for tx in results if tx]
            
    response = {
        "user_info": user["name"],
        "transaction_count": len(enriched_txs),
        "transactions": enriched_txs
    }
    
    # Bottleneck #4: Fixed Memory Leak
    # Use a unique key as before, but bound the dictionary size.
    unique_request_id = f"{request.url}_{time.time()}"
    analytics_data[unique_request_id] = {
        "user_id": user_id,
        "tx_count": len(enriched_txs)
    }
    
    # Simple eviction policy: remove oldest item if limit exceeded
    if len(analytics_data) > MAX_ANALYTICS_ENTRIES:
        first_key = next(iter(analytics_data))
        del analytics_data[first_key]
    
    return response
