from datetime import timedelta

from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.refresh_token import RefreshToken
from app.dependencies import get_current_user, rate_limit_login
from app.security import jwt_handler
from app.schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse, UserOut
from app.services import auth_service
from hashlib import sha256
from fastapi.exceptions import HTTPException

router = APIRouter()

REFRESH_COOKIE_NAME = "refresh_token"


@router.post("/register", response_model=UserOut, status_code=201)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register(body.email, body.password, db)


@router.post("/login", response_model=TokenResponse, dependencies=[Depends(rate_limit_login)])
def login(body: LoginRequest, response: Response, db: Session = Depends(get_db)):
    access_token,user_id= auth_service.login(body.email, body.password, db)
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=auth_service.create_refresh_token(user_id, db),
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=int(timedelta(days=settings.JWT_REFRESH_EXPIRE_DAYS).total_seconds()),
    )
    return TokenResponse(access_token=access_token, expires_in=settings.JWT_ACCESS_EXPIRE_MINUTES * 60)


@router.post("/refresh", response_model=TokenResponse)
def refresh(request : Request, response: Response, db: Session = Depends(get_db)):
    raw_token =request.cookies.get(REFRESH_COOKIE_NAME)
    if raw_token is None:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    token_hash = sha256(raw_token.encode()).hexdigest()
    query = db.query(RefreshToken).filter_by(token_hash=token_hash).first()
    if query is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    verfied,_= auth_service.verify_refresh_token(query.token_hash, db)
    if not verfied:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    acess_token = jwt_handler.create_access_token(sub=query.user_id)
    auth_service.revoke_refresh_token(query.token_hash, db)
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=auth_service.create_refresh_token(query.user_id, db),
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=int(timedelta(days=settings.JWT_REFRESH_EXPIRE_DAYS).total_seconds()),
    )    
    return TokenResponse(access_token=acess_token, expires_in=settings.JWT_ACCESS_EXPIRE_MINUTES * 60)

@router.post("/logout", status_code=204)
def logout(response: Response, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(RefreshToken).filter_by(user_id=current_user.id).all()
    for token in query:
        auth_service.revoke_refresh_token(token.token_hash, db)
    response.delete_cookie(REFRESH_COOKIE_NAME)


@router.get("/me", response_model=UserOut)
def me(current_user=Depends(get_current_user)):
    return current_user
