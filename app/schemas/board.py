from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Base DTO
class BoardBase(BaseModel):
    title: str
    content: str

# 생성 DTO
class BoardCreate(BoardBase):
    pass

# 수정 DTO
class BoardUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# 응답 DTO
class BoardResponse(BoardBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)