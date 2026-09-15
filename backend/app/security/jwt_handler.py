from datetime import timedelta, datetime

from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from fastapi import HTTPException

from app.config import settings

# HS256-signed JWT access tokens. Short expiry forces the frontend through
# /auth/refresh regularly instead of trusting one token indefinitely.


def create_access_token(sub: int) -> str:
    payload = {"sub": str(sub), "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_EXPIRE_MINUTES)}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")


def decode(token: str):
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="invalid token")
