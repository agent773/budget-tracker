# /api/auth/*
#
# POST /register (public, first-run only) -> auth_service.register
# POST /login (public, rate-limited) -> auth_service.login, set refresh-token cookie
# POST /refresh -> issue new access token from the refresh cookie
# POST /logout (auth) -> revoke refresh token, clear cookie
# GET  /me (auth) -> current user
from fastapi import APIRouter, Depends, HTTPException
import httpx

router = APIRouter

