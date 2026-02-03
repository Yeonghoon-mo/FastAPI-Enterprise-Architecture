import httpx
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from app.core.config import settings
from app.core import security
from app.repository import user_repository
from app.models.user import User
from app.core.redis import redis_client

# [Spring: KakaoAuthService]

KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USERINFO_URL = "https://kapi.kakao.com/v2/user/me"

async def get_kakao_auth_url():
    """카카오 로그인 페이지로 리다이렉트할 URL 생성"""
    params = {
        "client_id": settings.KAKAO_CLIENT_ID,
        "redirect_uri": settings.KAKAO_REDIRECT_URI,
        "response_type": "code",
    }
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{KAKAO_AUTH_URL}?{query_string}"

async def authenticate_kakao_user(db: AsyncSession, code: str):
    """카카오 인가 코드로 유저 정보를 가져와서 로그인 처리"""
    
    # 1. Authorization Code -> Access Token 교환
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            KAKAO_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "client_id": settings.KAKAO_CLIENT_ID,
                "client_secret": settings.KAKAO_CLIENT_SECRET, # 선택 사항이지만 설정했다면 필수
                "redirect_uri": settings.KAKAO_REDIRECT_URI,
                "code": code,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
        )
        
        if token_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to get access token from Kakao: {token_response.text}"
            )
        
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        
        # 2. Access Token -> 유저 정보 가져오기
        userinfo_response = await client.get(
            KAKAO_USERINFO_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
            }
        )
        
        if userinfo_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user info from Kakao"
            )
            
        user_info = userinfo_response.json()
        kakao_account = user_info.get("kakao_account", {})
        email = kakao_account.get("email")
        profile = kakao_account.get("profile", {})
        profile_image = profile.get("profile_image_url")
        
        if not email:
            # 카카오는 이메일이 선택 동의인 경우가 많아서, 식별자로 사용할 수 있게 처리 필요
            # 여기서는 편의상 ID를 이용한 가상 이메일 형식을 사용하거나 에러 처리
            email = f"{user_info.get('id')}@kakao.user"

        # 3. 우리 DB에 유저가 있는지 확인
        user = await user_repository.get_user(db, email=email)
        
        if not user:
            # 4. 없으면 신규 회원가입 (소셜 전용 유저)
            new_user = User(
                email=email,
                password=None,
                provider="kakao",
                social_id=str(user_info.get("id")),
                profile_image_url=profile_image,
                is_active=True
            )
            user = await user_repository.create_user(db, new_user)
        else:
            # 기존 유저 정보 업데이트
            user.provider = "kakao"
            user.social_id = str(user_info.get("id"))
            if profile_image:
                user.profile_image_url = profile_image
            await db.commit()
            await db.refresh(user)

        # 5. 자체 JWT 토큰 발급
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        our_access_token = security.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        # Redis에 세션 저장
        ttl_seconds = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        await redis_client.set(f"session:{user.email}", our_access_token, ex=ttl_seconds)
        
        return {"access_token": our_access_token, "token_type": "bearer"}
