from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

# Base DTO
class CommentBase(BaseModel):
    content: str = Field(..., description="댓글 내용", examples=["좋은 정보 감사합니다!"])

# 생성 DTO
class CommentCreate(CommentBase):
    """댓글 생성 시 필요한 데이터"""
    pass

# 수정 DTO
class CommentUpdate(BaseModel):
    """댓글 수정 시 필요한 데이터"""
    content: str = Field(..., description="수정할 댓글 내용", examples=["내용을 수정해봤어요."])

# 응답 DTO
class CommentResponse(CommentBase):
    """댓글 조회 시 반환되는 상세 데이터"""
    id: int = Field(..., description="댓글 고유 식별 번호 (PK)", examples=[1])
    board_id: int = Field(..., description="연관된 게시글 ID", examples=[10])
    user_id: str = Field(..., description="작성자의 이메일 주소", examples=["testuser@example.com"])
    created_at: datetime = Field(..., description="최초 작성 일시")
    updated_at: Optional[datetime] = Field(None, description="최종 수정 일시")

    model_config = ConfigDict(from_attributes=True)
