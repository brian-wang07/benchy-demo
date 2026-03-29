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
    
    # Use asyncio.sleep to yield control back to the event loop, 
    # allowing other requests to be processed concurrently.
    await asyncio.sleep(0.2) 
    
    user = database.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Resolve N+1 query pattern by fetching transactions in parallel via a thread pool.
    # This is significantly faster than sequential calls, especially with I/O churn.
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
    
    # Optimization: Prevent unbounded memory leak by capping the cache size
    if len(analytics_data) > 1000:
        # Remove the oldest entry (FIFO) to keep memory usage stable
        first_key = next(iter(analytics_data))
        del analytics_data[first_key]

    unique_request_id = f"{request.url}_{time.time()}"
    analytics_data[unique_request_id] = {
        "user_id": user_id,
        "tx_count": len(enriched_txs)
    }
    
    return response
