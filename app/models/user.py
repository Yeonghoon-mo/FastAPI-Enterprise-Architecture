from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship
from app.core.database import Base

# [JPA: @Entity]
class User(Base):
    # [JPA: @Table(name = "users")]
    __tablename__ = "users"

    # [JPA: @Id]
    # 이메일을 PK로 사용합니다.
    email = Column(String(255), primary_key=True, index=True)

    # [JPA: @Column]
    # 컬럼명을 hashed_password -> password 로 변경했습니다.
    password = Column(String(255))

    # [JPA: @Column(columnDefinition = "TINYINT(1) default 1")]
    is_active = Column(Boolean, default=True)

    # [JPA: @OneToMany(mappedBy = "owner")]
    boards = relationship("Board", back_populates="owner")