from sqlalchemy import Column, Integer, String, Boolean

from database import Base

class User(Base):
    # DB 테이블 이름 (@Table(name="users"))
    __tablename__ = "users"

    # @Id, @GeneratedValue
    id = Column(Integer, primary_key=True, index=True)
    # @Column(unique=true)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)

    # 만약, 관계 설정이 필요하면 relationship 사용 (JPA의 @OneToMany 와 같은 느낌)
    # items = relationship("Item", back_populates="owner")