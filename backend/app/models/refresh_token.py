# Server-side, revocable refresh tokens -- one row per active login session.
# This is what lets your phone and laptop each hold their own session without
# logging the other out (see auth_router.py's /login, /refresh, /logout TODOs).
#
# Fields: user_id (FK -> users.id), token_hash (store a HASH of the token,
# never the raw value -- same reasoning as password_hash on User), expires_at,
# revoked (bool, default False), created_at.
#
# Lookup pattern: hash the raw token value from the cookie, then query by
# token_hash -- never query by the raw token itself (same idea as passwords:
# if the DB leaks, raw tokens leaking would let someone impersonate any session).


from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

from app.database import Base


class RefreshToken(Base):
    __tablename__ = "RefreshToken"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id"), nullable=False)
    token_hash = Column(String, nullable=False)
    revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=7))
