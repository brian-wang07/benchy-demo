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
    
    # Bottleneck #1: Blocking the Async Event Loop
    # Simulated synchronous work (e.g., synchronous auth check or heavy CPU computation).
    # Because this route is `async def`, `time.sleep` blocks the single event loop thread,
    # hanging all other concurrent requests. Concurrency scaling is zeroed out.
    import asyncio
    await asyncio.sleep(0.2) 
    
    user = database.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    enriched_txs = []
    
    # Bottleneck #3: N+1 Query Anti-Pattern
    # Loops and makes separate DB calls per transaction. 
    # Combined with the file churn in database.py, this is a massive performance floor.
    for tx_id in user["transactions"]:
        tx_data = database.get_transaction(tx_id)
        if tx_data:
            enriched_txs.append(tx_data)
            
    response = {
        "user_info": user["name"],
        "transaction_count": len(enriched_txs),
        "transactions": enriched_txs
    }
    
    # Bottleneck #4: Memory Leak
    # request.url captures unique query strings or paths, making the dictionary grow forever
    # while retaining historical data indefinitely.
    unique_request_id = f"{request.url}_{time.time()}"
    analytics_data[unique_request_id] = {
        "user_id": user_id,
        "tx_count": len(enriched_txs)
    }
    
    return response
