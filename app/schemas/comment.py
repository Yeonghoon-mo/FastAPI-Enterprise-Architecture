from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Base DTO
class CommentBase(BaseModel):
    content: str

# 생성 DTO
class CommentCreate(CommentBase):
    pass

# 수정 DTO
class CommentUpdate(BaseModel):
    content: str

# 응답 DTO
class CommentResponse(CommentBase):
    id: int
    board_id: int
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
