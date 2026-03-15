from fastapi import FastAPI, Request, HTTPException
import time
import database
import asyncio

app = FastAPI()

# Global dictionary used as a naive analytics cache
analytics_data = {}

@app.get("/user/{user_id}/dashboard")
async def user_dashboard(user_id: str, request: Request):
    """
    Endpoint mapping a user's dashboard.
    """
    
    # Non-blocking simulated delay
    await asyncio.sleep(0.2) 
    
    # Offload sync DB call to thread
    user = await asyncio.to_thread(database.get_user, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Concurrently fetch transactions to mitigate N+1 delay
    tx_tasks = [asyncio.to_thread(database.get_transaction, tx_id) for tx_id in user["transactions"]]
    tx_results = await asyncio.gather(*tx_tasks)
    
    enriched_txs = [tx for tx in tx_results if tx]
            
    response = {
        "user_info": user["name"],
        "transaction_count": len(enriched_txs),
        "transactions": enriched_txs
    }
    
    unique_request_id = f"{request.url}_{time.time()}"
    analytics_data[unique_request_id] = {
        "user_id": user_id,
        "tx_count": len(enriched_txs)
    }
    
    # Prevent unbounded memory leak
    if len(analytics_data) > 10000:
        analytics_data.pop(next(iter(analytics_data)))
    
    return response
