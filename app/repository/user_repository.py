import base64
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

# [Spring: @Repository]

# PK(Email)로 유저 조회
def get_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# 유저 생성 (Base64 Encoding 적용)
def create_user(db: Session, user: UserCreate):
    # 비밀번호를 Base64로 인코딩 (UTF-8 bytes -> Base64 bytes -> String)
    encoded_password = base64.b64encode(user.password.encode('utf-8')).decode('utf-8')
    
    db_user = User(email=user.email, password=encoded_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# 유저 수정 (Update)
def update_user(db: Session, db_user: User, user_update: UserUpdate):
    # 비밀번호 변경 요청이 있다면 Base64 인코딩 후 적용
    if user_update.password:
        encoded_password = base64.b64encode(user_update.password.encode('utf-8')).decode('utf-8')
        db_user.password = encoded_password
    
    # 활성 상태 변경 요청이 있다면 적용
    if user_update.is_active is not None:
        db_user.is_active = user_update.is_active
        
    db.commit()
    db.refresh(db_user)
    return db_user

# 유저 삭제 (Delete)
def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()