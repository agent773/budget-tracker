from datetime import timedelta

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.refresh_token import RefreshToken
from app.dependencies import get_current_user, rate_limit_login
from app.schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse, UserOut
from app.services import auth_service
from security.password_hasher import hash

router = APIRouter()

REFRESH_COOKIE_NAME = "refresh_token"


@router.post("/register", response_model=UserOut, status_code=201)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register(body.email, body.password, db)


@router.post("/login", response_model=TokenResponse, dependencies=[Depends(rate_limit_login)])
def login(body: LoginRequest, response: Response, db: Session = Depends(get_db)):
    access_token = auth_service.login(body.email, body.password, db)

    # TODO: there's no RefreshToken table yet (see plan's data model -- it was
    # described in prose but never actually added as a table). Until it exists,
    # this cookie isn't backed by anything real and /refresh below can't work.
    # Options: add a small `refresh_tokens` table (id, user_id, token_hash,
    # expires_at, revoked) so multiple devices (phone + laptop) can each hold
    # their own session -- a single token on the User row would log one out
    # whenever the other logs in.
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value="re",
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=int(timedelta(days=settings.JWT_REFRESH_EXPIRE_DAYS).total_seconds()),
    )
    return TokenResponse(access_token=access_token, expires_in=settings.JWT_ACCESS_EXPIRE_MINUTES * 60)


@router.post("/refresh", response_model=TokenResponse)
def refresh(response: Response, db: Session = Depends(get_db)):
    hashed_refresh_token = hash(response.key)
    # TODO: read REFRESH_COOKIE_NAME from the incoming request, hash it, look it
    # up against the refresh_tokens table, 401 if missing/expired/revoked,
    # then jwt_handler.create_access_token(sub=token.user_id). Optionally
    # rotate: revoke the old row, set a new cookie, same as login() above.
    raise NotImplementedError


@router.post("/logout", status_code=204)
def logout(response: Response, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    # TODO: mark this user's refresh_tokens row(s) revoked in the DB -- clearing
    # the cookie alone doesn't invalidate a copy of the token an attacker has.
    response.delete_cookie(REFRESH_COOKIE_NAME)


@router.get("/me", response_model=UserOut)
def me(current_user=Depends(get_current_user)):
    return current_user
