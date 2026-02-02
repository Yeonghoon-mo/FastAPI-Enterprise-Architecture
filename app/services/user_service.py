from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repository import user_repository
from app.schemas.user import UserCreate

# [Spring: @Service]
# 비즈니스 로직을 담당하는 계층입니다.
# Controller(Router)와 Repository 사이에서 중재자 역할을 합니다.

def create_user(db: Session, user: UserCreate):
    # 1. 중복 이메일 체크 (Business Logic)
    # [Spring: if (userRepository.findByEmail(email).isPresent()) throw ...]
    db_user = user_repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. 유저 생성 (Repository 호출)
    return user_repository.create_user(db=db, user=user)

def get_user(db: Session, user_id: int):
    # 1. 유저 조회
    db_user = user_repository.get_user(db, user_id=user_id)
    
    # 2. 존재 여부 체크 (Business Logic)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    return db_user
