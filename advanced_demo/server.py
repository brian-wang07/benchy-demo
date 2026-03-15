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
    
    # Bottleneck #1: Fixed blocking the Async Event Loop
    # Replacing time.sleep (blocking) with asyncio.sleep (non-blocking)
    await asyncio.sleep(0.2) 
    
    user = database.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    import asyncio

    # Optimization for Bottleneck #3: N+1 Query Anti-Pattern
    # Execute synchronous database calls in parallel threads to avoid blocking the loop 
    # and to reduce total execution time from O(N) to O(1) concurrent wait.
    tasks = [asyncio.to_thread(database.get_transaction, tx_id) for tx_id in user["transactions"]]
    results = await asyncio.gather(*tasks)
    enriched_txs = [tx for tx in results if tx]
            
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
