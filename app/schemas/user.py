from pydantic import BaseModel, ConfigDict
from typing import Optional

# [DTO: Data Transfer Object]

# 1. 공통 속성 (Base DTO)
class UserBase(BaseModel):
    email: str

# 2. 생성 요청 DTO (Request Body)
class UserCreate(UserBase):
    password: str

# 3. 수정 요청 DTO (Request Body) - [New!]
class UserUpdate(BaseModel):
    password: Optional[str] = None
    is_active: Optional[bool] = None

# 4. 응답 DTO (Response Body)
class User(UserBase):
    is_active: bool

    # [ModelMapper] Entity -> DTO 변환
    model_config = ConfigDict(from_attributes=True)
