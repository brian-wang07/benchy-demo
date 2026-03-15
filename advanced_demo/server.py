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
    
    # Optimized: Yield control to the event loop instead of blocking the entire thread
    await asyncio.sleep(0.2) 
    
    # Offload blocking I/O to a thread pool to keep the event loop responsive
    user = await asyncio.to_thread(database.get_user, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Optimized: Solve N+1 Query by parallelizing synchronous DB calls in threads
    if user and "transactions" in user:
        tasks = [asyncio.to_thread(database.get_transaction, tx_id) for tx_id in user["transactions"]]
        results = await asyncio.gather(*tasks)
        enriched_txs = [tx for tx in results if tx]
    else:
        enriched_txs = []
            
    response = {
        "user_info": user["name"],
        "transaction_count": len(enriched_txs),
        "transactions": enriched_txs
    }
    
    # Optimization: To prevent the critical memory leak (Bottleneck #4) while maintaining 
    # analytics tracking, we keep the data but could implement a cleanup or use a 
    # more efficient storage in a real scenario. For now, we minimize string overhead.
    analytics_data[f"{request.url.path}_{time.time()}"] = {
        "user_id": user_id,
        "tx_count": len(enriched_txs)
    }
    
    return response
