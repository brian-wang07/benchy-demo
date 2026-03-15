import asyncio
from fastapi import FastAPI, Request, HTTPException
import time
import database

app = FastAPI()

# Global dictionary used as a naive analytics cache
analytics_data = {}

@app.get("/user/{user_id}/dashboard")
async def user_dashboard(user_id: str, request: Request):
    """
    Endpoint mapping a user's dashboard.
    """
    
    # Non-blocking sleep allows the event loop to handle other requests concurrently
    await asyncio.sleep(0.2) 
    
    # Offload sync DB call to a thread to avoid blocking the event loop
    user = await asyncio.to_thread(database.get_user, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    enriched_txs = []
    tx_ids = user.get("transactions", [])
    
    # Parallelize transaction fetches using asyncio.gather and thread offloading
    if tx_ids:
        tx_results = await asyncio.gather(
            *(asyncio.to_thread(database.get_transaction, tx_id) for tx_id in tx_ids)
        )
        enriched_txs = [tx for tx in tx_results if tx]
            
    response = {
        "user_info": user["name"],
        "transaction_count": len(enriched_txs),
        "transactions": enriched_txs
    }
    
    # Maintain cache size to prevent unbounded memory growth
    if len(analytics_data) >= 5000:
        # dicts are ordered in Python 3.7+, so this prunes the oldest entry
        analytics_data.pop(next(iter(analytics_data)))

    # Use a more efficient key and store analytics
    analytics_data[f"{user_id}_{time.time()}"] = {
        "user_id": user_id,
        "tx_count": len(enriched_txs)
    }
    
    return response
