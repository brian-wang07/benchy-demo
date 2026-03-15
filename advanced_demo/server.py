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
    
    # Fixed: Use non-blocking sleep to keep the event loop free for other requests
    await asyncio.sleep(0.2) 
    
    user = database.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Optimized: Use a bulk fetch to avoid the N+1 query problem.
    # This reduces file I/O operations from O(N) to O(1).
    tx_ids = user.get("transactions", [])
    enriched_txs = [tx for tx in database.get_transactions(tx_ids) if tx]
            
    response = {
        "user_info": user["name"],
        "transaction_count": len(enriched_txs),
        "transactions": enriched_txs
    }
    
    # Optimized: Fixed memory leak by using a stable key (user_id).
    # This bounds the dictionary size and prevents it from growing indefinitely.
    analytics_data[user_id] = {
        "last_tx_count": len(enriched_txs),
        "last_accessed": time.time()
    }
    
    return response
