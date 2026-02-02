from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

# [JPA: @Entity]
class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    content = Column(Text)
    
    # user_id는 users 테이블의 email 컬럼을 참조합니다.
    user_id = Column(String(255), ForeignKey("users.email"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # [JPA: 양방향 매핑]
    owner = relationship("User", back_populates="boards")