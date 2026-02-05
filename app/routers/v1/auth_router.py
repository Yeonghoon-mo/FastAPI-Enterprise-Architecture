from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.token import Token
from app.services import auth_service, google_auth_service, kakao_auth_service
from app.core.dependencies import get_current_user
from app.models.user import User
from app.core.rate_limiter import RateLimiter

router = APIRouter(tags=["authentication"])

# [Google 로그인 시작 API]
@router.get(
    "/auth/google", 
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
    summary="Google 로그인 시작",
    description="사용자를 Google OAuth2 로그인 페이지로 리다이렉트합니다. **1분에 5회**로 요청이 제한됩니다.",
    responses={
        307: {"description": "Google 로그인 페이지로 리다이렉트 성공"},
        429: {"description": "요청 횟수 초과"}
    }
)
async def google_login():
    """Google 로그인 페이지로 리다이렉트"""
    auth_url = await google_auth_service.get_google_auth_url()
    return RedirectResponse(url=auth_url)

# [Google 로그인 콜백 API]
@router.get(
    "/auth/google/callback", 
    response_model=Token, 
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
    summary="Google 로그인 콜백",
    description="Google 인증 완료 후 받은 코드를 사용하여 자체 JWT 토큰을 발급합니다.",
    responses={
        200: {"description": "인증 성공 및 토큰 발급"},
        400: {"description": "유효하지 않은 인증 코드"},
        401: {"description": "Google 인증 실패"},
        429: {"description": "요청 횟수 초과"}
    }
)
async def google_callback(code: str, db: AsyncSession = Depends(get_db)):
    """Google 인증 후 자체 토큰 발급"""
    return await google_auth_service.authenticate_google_user(db=db, code=code)

# [Kakao 로그인 시작 API]
@router.get(
    "/auth/kakao", 
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
    summary="Kakao 로그인 시작",
    description="사용자를 Kakao OAuth2 로그인 페이지로 리다이렉트합니다. **1분에 5회**로 요청이 제한됩니다.",
    responses={
        307: {"description": "Kakao 로그인 페이지로 리다이렉트 성공"},
        429: {"description": "요청 횟수 초과"}
    }
)
async def kakao_login():
    """카카오 로그인 페이지로 리다이렉트"""
    auth_url = await kakao_auth_service.get_kakao_auth_url()
    return RedirectResponse(url=auth_url)

# [Kakao 로그인 콜백 API]
@router.get(
    "/auth/kakao/callback", 
    response_model=Token, 
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
    summary="Kakao 로그인 콜백",
    description="Kakao 인증 완료 후 받은 코드를 사용하여 자체 JWT 토큰을 발급합니다.",
    responses={
        200: {"description": "인증 성공 및 토큰 발급"},
        400: {"description": "유효하지 않은 인증 코드"},
        401: {"description": "Kakao 인증 실패"},
        429: {"description": "요청 횟수 초과"}
    }
)
async def kakao_callback(code: str, db: AsyncSession = Depends(get_db)):
    """카카오 인증 후 자체 토큰 발급"""
    return await kakao_auth_service.authenticate_kakao_user(db=db, code=code)

# [로그아웃 API]
@router.post(
    "/logout", 
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="사용자 로그아웃",
    description="현재 세션을 만료시키고 Redis에서 토큰을 제거합니다. **1분에 10회**로 요청이 제한됩니다.",
    responses={
        200: {"description": "로그아웃 성공"},
        401: {"description": "인증 실패 (이미 로그아웃되었거나 유효하지 않은 토큰)"},
        429: {"description": "요청 횟수 초과"}
    }
)
async def logout(current_user: User = Depends(get_current_user)):
    """로그아웃 처리 (세션 삭제)"""
    return await auth_service.logout(email=current_user.email)