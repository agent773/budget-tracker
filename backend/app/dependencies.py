# Shared FastAPI dependencies, injected via Depends(...) in routers.
#
# get_current_user(token, db): decode the JWT (401 on invalid/expired), look up
# the user, 401 if missing/inactive. Import into routers as Depends(get_current_user).
#
# rate_limit_login(request): 429 if this IP has exceeded the login attempt limit
# (security/rate_limiter.py).
from fastapi import Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.status import HTTP_429_TOO_MANY_REQUESTS
from typing import Annotated
from security.jwt_handler import decode
import time


def get_current_user(token: Annotated[str, Depends]):
    user = decode(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
            )
    return user

request_counts = {}

async def rate_limit_login(request:Request, call_next):
    client_ip = request.client.host
    now = time.time()
    window = 60  # seconds
    max_requests = 10
    
    timestamps = request_counts.get(client_ip, [])
    timestamps = [t for t in timestamps if now - t < window]
    
    if len(timestamps) >= max_requests:
        return JSONResponse(
            status_code=HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Too many requests"}
            )
    timestamps.append(now)
    request_counts[client_ip] = timestamps
    return await call_next(request) 
    