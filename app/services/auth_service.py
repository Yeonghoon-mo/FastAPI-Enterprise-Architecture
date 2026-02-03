from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.core import security
from app.core.config import settings
from app.repository import user_repository
from app.core.redis import redis_client

# [Spring: AuthService]

async def login(db: AsyncSession, form_data):
    # 1. 유저 확인
    user = await user_repository.get_user(db, email=form_data.username)
    
    # 2. 비밀번호 검증
    if not user or not security.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. 토큰 발급
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # 4. Redis에 세션 저장 (중복 로그인 방지 or 유효성 검사 목적)
    # Key: session:{email} / Value: access_token / TTL: Token Expiration
    ttl_seconds = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    await redis_client.set(f"session:{user.email}", access_token, ex=ttl_seconds)
    
    return {"access_token": access_token, "token_type": "bearer"}

async def logout(email: str):
    # Redis에서 세션 삭제
    await redis_client.delete(f"session:{email}")
    return {"message": "Successfully logged out"}