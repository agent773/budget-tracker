# Shared FastAPI dependencies, injected via Depends(...) in routers.
#
# get_current_user(token, db): decode the JWT (401 on invalid/expired), look up
# the user, 401 if missing/inactive. Import into routers as Depends(get_current_user).
#
# rate_limit_login(request): 429 if this IP has exceeded the login attempt limit
# (security/rate_limiter.py).
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from typing import Annotated
from app.security.jwt_handler import decode
from app.models.user import User
from sqlalchemy.orm import Session
from app.database import get_db
import time

ringbear = HTTPBearer()

def get_current_user(token: Annotated[HTTPAuthorizationCredentials, Depends(ringbear)],db: Session = Depends(get_db)):
    #payload = decode(token)
    token = creds.credentials
    user_can = db.query(User).get(int(token))
    if not user_can:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
            )
    return user_can

request_counts = {}

async def rate_limit_login(request:Request):
    client_ip = request.client.host
    now = time.time()
    window = 60  # seconds
    max_requests = 10
    
    timestamps = request_counts.get(client_ip, [])
    timestamps = [t for t in timestamps if now - t < window]
    
    if len(timestamps) >= max_requests:
        raise HTTPException(status_code=429,detail = "Too many requests, Gotta go Fast is not a health condition")
    timestamps.append(now)
    request_counts[client_ip] = timestamps