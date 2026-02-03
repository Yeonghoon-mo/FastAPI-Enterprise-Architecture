from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.token import Token
from app.services import auth_service
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(tags=["authentication"])

# [로그인 API]
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    return await auth_service.login(db=db, form_data=form_data)

# [로그아웃 API]
@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    return await auth_service.logout(email=current_user.email)
