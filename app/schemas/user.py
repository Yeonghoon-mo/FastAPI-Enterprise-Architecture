from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from app.models.user import UserRole

# [DTO: Data Transfer Object]

# 1. 공통 속성 (Base DTO)
class UserBase(BaseModel):
    # 이메일 정규식 유효성 검사 추가
    email: str = Field(
        ..., 
        pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        description="사용자의 이메일 주소 (고유 식별자)",
        examples=["testuser@example.com"]
    )
    role: UserRole = Field(
        default=UserRole.USER, 
        description="사용자의 권한 역할 (ADMIN, USER, GUEST)",
        examples=[UserRole.USER]
    )

# 2. 생성 요청 DTO (Request Body)
class UserCreate(UserBase):
    password: Optional[str] = Field(
        None, 
        min_length=8, 
        description="비밀번호 (소셜 가입 시 생략 가능, 일반 가입 시 최소 8자)",
        examples=["password123!"]
    )

# 3. 수정 요청 DTO (Request Body)
class UserUpdate(BaseModel):
    password: Optional[str] = Field(
        None, 
        min_length=8, 
        description="새 비밀번호",
        examples=["newpassword123!"]
    )
    is_active: Optional[bool] = Field(
        None, 
        description="계정 활성화 상태 여부",
        examples=[True]
    )
    role: Optional[UserRole] = Field(
        None, 
        description="변경할 권한 역할",
        examples=[UserRole.ADMIN]
    )

# 4. 응답 DTO (Response Body)
class User(UserBase):
    is_active: bool = Field(..., description="사용자 활성 상태")
    profile_image_url: Optional[str] = Field(None, description="프로필 이미지 URL 경로")

    # [ModelMapper] Entity -> DTO 변환
    model_config = ConfigDict(from_attributes=True)
