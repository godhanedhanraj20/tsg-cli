import os
from time import time
from fastapi import Header, HTTPException, Request

API_TOKEN = os.getenv("TSG_API_TOKEN", "dev-secret-key")
_requests = {}

async def verify_token(x_api_key: str = Header(None)):
    if x_api_key != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

def rate_limit(request: Request):
    ip = request.client.host if request.client else "unknown"
    now = time()
    window = 10

    if ip not in _requests:
        _requests[ip] = []

    _requests[ip] = [t for t in _requests[ip] if now - t < window]

    if len(_requests[ip]) > 20:
        raise HTTPException(status_code=429, detail="Too many requests")

    _requests[ip].append(now)
