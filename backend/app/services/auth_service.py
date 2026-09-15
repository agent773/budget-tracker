from fastapi import HTTPException

from app.security import jwt_handler, password_hasher
from app.models.user import User

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


def login(email: str, password: str, db) -> str:
    user = db.query(User).filter_by(email=email).first()
    if user is None or not password_hasher.verify(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return jwt_handler.create_access_token(sub=user.id)
