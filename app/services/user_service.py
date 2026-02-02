from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repository import user_repository
from app.schemas.user import UserCreate, UserUpdate

# [Spring: @Service]

def create_user(db: Session, user: UserCreate):
    db_user = user_repository.get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일 계정입니다.")
    
    return user_repository.create_user(db=db, user=user)

def get_user(db: Session, email: str):
    db_user = user_repository.get_user(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="해당 Email의 유저가 존재하지 않습니다.")
    return db_user

# 유저 수정
def update_user(db: Session, email: str, user_update: UserUpdate):
    # 1. 수정할 유저가 존재하는지 확인
    db_user = get_user(db, email) # 없으면 여기서 404 발생
    
    # 2. 업데이트 수행
    return user_repository.update_user(db=db, db_user=db_user, user_update=user_update)

# 유저 삭제
def delete_user(db: Session, email: str):
    # 1. 삭제할 유저가 존재하는지 확인
    db_user = get_user(db, email) # 없으면 여기서 404 발생
    
    # 2. 삭제 수행
    user_repository.delete_user(db=db, db_user=db_user)
    return {"message": "User deleted successfully"}
