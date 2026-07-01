import time
from fastapi import FastAPI, Request

app = FastAPI()

# 1. Initialize In-Memory Metrics State
START_TIME = time.time()
METRICS_STATE = {
    "total_requests": 0,
    "total_analyses": 0,
    "version": "1.0.0"
}


# 2. Request Tracking Middleware (Keep 2 blank lines above)
@app.middleware("http")
async def count_requests_middleware(request: Request, call_next):
    """Middleware to count incoming application requests."""
    # Skip tracking requests hitting the metrics endpoint itself
    if request.url.path != "/metrics":
        METRICS_STATE["total_requests"] += 1
        
        # Safely increment analyses if your app logic triggers an analysis path
        if "/analyze" in request.url.path:
            METRICS_STATE["total_analyses"] += 1
            
    response = await call_next(request)
    return response


# 3. Metrics Route Endpoint (Keep 2 blank lines above)
@app.get("/metrics")
async def get_metrics():
    """Returns application metrics tracking total usage statistics."""
    uptime_seconds = int(time.time() - START_TIME)
    
    # Format uptime cleanly into an understandable string
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_string = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    return {
        "requests": METRICS_STATE["total_requests"],
        "analyses": METRICS_STATE["total_analyses"],
        "uptime": uptime_string,
        "version": METRICS_STATE["version"]
    }
