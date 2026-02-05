from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

# Base DTO
class BoardBase(BaseModel):
    title: str = Field(..., description="게시글 제목", examples=["FastAPI로 엔터프라이즈 서버 만들기"])
    content: str = Field(..., description="게시글 본문 내용", examples=["Spring Boot의 구조를 이식한 견고한 아키텍처 가이드..."])

# 생성 DTO
class BoardCreate(BoardBase):
    """게시글 생성 시 필요한 데이터"""
    pass

# 수정 DTO
class BoardUpdate(BaseModel):
    """게시글 수정 시 선택적으로 제공할 데이터"""
    title: Optional[str] = Field(None, description="수정할 게시글 제목", examples=["수정된 제목"])
    content: Optional[str] = Field(None, description="수정할 게시글 본문 내용", examples=["내용도 좀 바꿔볼까요?"])

# 응답 DTO
class BoardResponse(BoardBase):
    """게시글 조회 시 반환되는 상세 데이터"""
    id: int = Field(..., description="게시글 고유 식별 번호 (PK)", examples=[1])
    user_id: str = Field(..., description="작성자의 이메일 주소", examples=["testuser@example.com"])
    image_url: Optional[str] = Field(None, description="첨부 이미지 URL 경로", examples=["/static/uploads/boards/abc.jpg"])
    created_at: datetime = Field(..., description="최초 작성 일시")
    updated_at: Optional[datetime] = Field(None, description="최종 수정 일시")

    model_config = ConfigDict(from_attributes=True)