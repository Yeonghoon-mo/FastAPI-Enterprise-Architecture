from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, User, UserUpdate
from app.services import user_service

# [Spring: @RestController]
router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# 회원가입 (POST /users)
@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db=db, user=user)

# 회원 조회 (GET /users/{email})
@router.get("/{email}", response_model=User)
def read_user(email: str, db: Session = Depends(get_db)):
    return user_service.get_user(db=db, email=email)

# 회원 수정 (PUT /users/{email})
@router.put("/{email}", response_model=User)
def update_user(email: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(db=db, email=email, user_update=user_update)

# 회원 삭제 (DELETE /users/{email})
@router.delete("/{email}")
def delete_user(email: str, db: Session = Depends(get_db)):
    return user_service.delete_user(db=db, email=email)