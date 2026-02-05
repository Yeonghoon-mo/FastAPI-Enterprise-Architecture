from pydantic import BaseModel, Field

# 토큰 응답 DTO
class Token(BaseModel):
    access_token: str = Field(..., description="JWT 액세스 토큰 문자열", examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])
    token_type: str = Field(..., description="토큰 타입 (일반적으로 Bearer)", examples=["Bearer"])

# 토큰 데이터 (Payload)
class TokenData(BaseModel):
    email: str | None = Field(None, description="토큰에 담긴 사용자 이메일 주소", examples=["testuser@example.com"])
