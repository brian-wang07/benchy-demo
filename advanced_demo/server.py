from fastapi import FastAPI, Request, HTTPException
import time
import database

app = FastAPI()

# Global dictionary used as a naive analytics cache
# Bottleneck #4: Unbounded memory leak
analytics_data = {}

@app.get("/user/{user_id}/dashboard")
async def user_dashboard(user_id: str, request: Request):
    """
    Endpoint mapping a user's dashboard.
    """
    
    # Fix Bottleneck #1: Use non-blocking sleep to keep the event loop free
    await asyncio.sleep(0.2) 
    
    # Offload synchronous DB call to a thread pool to avoid blocking the loop
    user = await run_in_threadpool(database.get_user, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Fix Bottleneck #3: Solve N+1 Query by parallelizing sync DB calls
    # This fetches all transactions concurrently instead of one-by-one
    tx_ids = user.get("transactions", [])
    tasks = [run_in_threadpool(database.get_transaction, tx_id) for tx_id in tx_ids]
    results = await asyncio.gather(*tasks)
    enriched_txs = [tx for tx in results if tx]
            
    response = {
        "user_info": user["name"],
        "transaction_count": len(enriched_txs),
        "transactions": enriched_txs
    }
    
    # Fix Bottleneck #4: Prevent Memory Leak with a size-limited cache
    unique_request_id = f"{request.url}_{time.time()}"
    if len(analytics_data) > 10000:
        # Remove oldest entry to maintain fixed memory footprint
        analytics_data.pop(next(iter(analytics_data)))
        
    analytics_data[unique_request_id] = {
        "user_id": user_id,
        "tx_count": len(enriched_txs)
    }
    
    return response
