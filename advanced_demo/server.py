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
    
    # Fix: Use non-blocking sleep to keep the event loop free
    await asyncio.sleep(0.2) 
    
    # Fix: Run synchronous DB call in a thread to avoid blocking the event loop
    user = await asyncio.to_thread(database.get_user, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Fix: Resolve N+1 query pattern by fetching all transactions in parallel
    tx_ids = user.get("transactions", [])
    if tx_ids:
        tasks = [asyncio.to_thread(database.get_transaction, tx_id) for tx_id in tx_ids]
        tx_results = await asyncio.gather(*tasks)
        enriched_txs = [tx for tx in tx_results if tx]
    else:
        enriched_txs = []
            
    response = {
        "user_info": user["name"],
        "transaction_count": len(enriched_txs),
        "transactions": enriched_txs
    }
    
    # Fix: Optimize key generation and mitigate memory leak
    # We keep the structure but avoid expensive string conversions where possible
    request_key = f"{id(request)}_{time.time_ns()}"
    analytics_data[request_key] = {
        "user_id": user_id,
        "tx_count": len(enriched_txs)
    }
    
    # Simple eviction to prevent unbounded growth (Bottleneck #4)
    if len(analytics_data) > 10000:
        # Remove oldest item (approximate)
        del analytics_data[next(iter(analytics_data))]
    
    return response
