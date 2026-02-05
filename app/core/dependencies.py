from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.config import settings
from app.repository import user_repository
from app.models.user import User, UserRole
from app.core.redis import redis_client

# 토큰을 직접 입력할 수 있는 Bearer Token 스키마 설정
security = HTTPBearer()

# [보안 의존성] 현재 로그인한 유저 가져오기
async def get_current_user(
    request: Request,
    auth: HTTPAuthorizationCredentials = Depends(security), 
    db: AsyncSession = Depends(get_db)
) -> User:
    token = auth.credentials
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
        
    # [추가] request.state에 유저 정보 저장 (RateLimiter 등에서 활용)
    request.state.user = user
        
    return user

# [RBAC 의존성] 특정 역할을 가진 유저만 허용
class RoleChecker:
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have enough permissions to access this resource"
            )
        return current_user

# 사용 예시:
# admin_only = RoleChecker([UserRole.ADMIN])
# user_only = RoleChecker([UserRole.ADMIN, UserRole.USER])