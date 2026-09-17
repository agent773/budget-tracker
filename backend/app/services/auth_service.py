from fastapi import HTTPException

from app.security import jwt_handler, password_hasher
from app.models.user import User
from app.models.refresh_token import RefreshToken
from secrets import token_urlsafe
from hashlib import sha256
from datetime import datetime



# Login always raises the same generic message for "no such user" and "wrong
# password" -- two different messages would let an attacker enumerate which
# emails are registered.


def register(email: str, password: str, db):
    existing = db.query(User).filter_by(email=email).first()
    if existing is not None:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(email=email, password_hash=password_hasher.hash(password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login(email: str, password: str, db) -> tuple[str, int]:
    user = db.query(User).filter_by(email=email).first()
    if user is None or not password_hasher.verify(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return jwt_handler.create_access_token(sub=user.id), user.id


def create_refresh_token(user_id: int,db):
    token = token_urlsafe(32)
    token_hash = sha256(token.encode()).hexdigest()
    new_refresh_token = RefreshToken(user_id=user_id,token_hash=token_hash)
    db.add(new_refresh_token)
    db.commit()
    db.refresh(new_refresh_token)
    return token

def verify_refresh_token(token_hash: str ,db):
    token = db.query(RefreshToken).filter_by(token_hash=token_hash).first()
    if token is None:
        return (None,False)
    if not token.revoked and not datetime.utcnow() > token.expires_at:
        return (token.user_id,True)
    return (token.user_id,False)

def revoke_refresh_token(token_hash: str ,db):
    token = db.query(RefreshToken).filter_by(token_hash=token_hash).first()
    if token is None:
        return None
    token.revoked = True
    db.commit()
