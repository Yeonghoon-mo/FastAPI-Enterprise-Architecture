from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.config import settings
from app.repository import user_repository
from app.models.user import User
from app.core.redis import redis_client

# 토큰을 추출할 엔드포인트 지정 (Swagger의 Authorize 버튼 활성화)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# [보안 의존성] 현재 로그인한 유저 가져오기
async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. 토큰 디코딩
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
            
        # 2. Redis 세션 검증 (로그아웃된 토큰인지 확인)
        cached_token = await redis_client.get(f"session:{email}")
        if cached_token is None or cached_token != token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session expired or logged out",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
    except JWTError:
        raise credentials_exception
        
    # 3. 유저 조회
    user = await user_repository.get_user(db, email=email)
    if user is None:
        raise credentials_exception
        
    return user