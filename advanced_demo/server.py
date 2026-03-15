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
    
    # Optimization: Use non-blocking sleep to allow the event loop to handle other requests
    await asyncio.sleep(0.2) 
    
    # Optimization: Run synchronous DB call in a thread pool to avoid blocking the event loop
    user = await asyncio.to_thread(database.get_user, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Optimization: Solve N+1 bottleneck by fetching all transactions concurrently
    # This transforms sequential blocking calls into parallel execution
    tasks = [asyncio.to_thread(database.get_transaction, tx_id) for tx_id in user["transactions"]]
    results = await asyncio.gather(*tasks)
    enriched_txs = [tx for tx in results if tx]
            
    response = {
        "user_info": user["name"],
        "transaction_count": len(enriched_txs),
        "transactions": enriched_txs
    }
    
    # Optimization: Prevent memory leak by bounding the analytics cache
    if len(analytics_data) > 10000:
        # Dictionary keys in Python 3.7+ are ordered; this removes the oldest entry (FIFO)
        del analytics_data[next(iter(analytics_data))]

    unique_request_id = f"{request.url}_{time.time()}"
    analytics_data[unique_request_id] = {
        "user_id": user_id,
        "tx_count": len(enriched_txs)
    }
    
    return response
