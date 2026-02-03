from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.token import Token
from app.services import auth_service, google_auth_service, kakao_auth_service
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(tags=["authentication"])

# [Google 로그인 시작 API]
@router.get("/auth/google")
async def google_login():
    """Google 로그인 페이지로 리다이렉트"""
    auth_url = await google_auth_service.get_google_auth_url()
    return RedirectResponse(url=auth_url)

# [Google 로그인 콜백 API]
@router.get("/auth/google/callback", response_model=Token)
async def google_callback(code: str, db: AsyncSession = Depends(get_db)):
    """Google 인증 후 자체 토큰 발급"""
    return await google_auth_service.authenticate_google_user(db=db, code=code)

# [Kakao 로그인 시작 API]
@router.get("/auth/kakao")
async def kakao_login():
    """카카오 로그인 페이지로 리다이렉트"""
    auth_url = await kakao_auth_service.get_kakao_auth_url()
    return RedirectResponse(url=auth_url)

# [Kakao 로그인 콜백 API]
@router.get("/auth/kakao/callback", response_model=Token)
async def kakao_callback(code: str, db: AsyncSession = Depends(get_db)):
    """카카오 인증 후 자체 토큰 발급"""
    return await kakao_auth_service.authenticate_kakao_user(db=db, code=code)

# [로그아웃 API]
@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """로그아웃 처리 (세션 삭제)"""
    return await auth_service.logout(email=current_user.email)