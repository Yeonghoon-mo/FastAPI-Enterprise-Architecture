from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

# [Spring: @Repository]

# PK(Email)로 유저 조회
async def get_user(db: AsyncSession, email: str):
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalars().first()

# 유저 생성 (비밀번호가 있는 경우만 BCrypt 적용)
async def create_user(db: AsyncSession, user: UserCreate | User):
    if isinstance(user, User):
        # 이미 User 모델 객체인 경우 (소셜 로그인 등)
        db_user = user
        if db_user.password:
            db_user.password = get_password_hash(db_user.password)
    else:
        # UserCreate DTO인 경우 (일반 회원가입 등)
        hashed_password = get_password_hash(user.password) if user.password else None
        db_user = User(
            email=user.email, 
            password=hashed_password,
            is_active=True
        )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user

# 유저 수정 (Update)
async def update_user(db: AsyncSession, db_user: User, user_update: UserUpdate):
    if user_update.password:
        db_user.password = get_password_hash(user_update.password)
    
    if user_update.is_active is not None:
        db_user.is_active = user_update.is_active
        
    await db.commit()
    await db.refresh(db_user)
    return db_user

# 유저 삭제 (Delete)
async def delete_user(db: AsyncSession, db_user: User):
    await db.delete(db_user)
    await db.commit()
