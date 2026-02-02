from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    
    # FK 설정
    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"))
    user_id = Column(String(255), ForeignKey("users.email"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 관계 설정
    board = relationship("Board", back_populates="comments")
    owner = relationship("User", back_populates="comments")
