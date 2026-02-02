from sqlalchemy import Boolean, Column, Integer, String
from app.core.database import Base

# [JPA: @Entity]
# 데이터베이스의 'users' 테이블과 매핑되는 클래스입니다.
class User(Base):
    # [JPA: @Table(name = "users")]
    __tablename__ = "users"

    # [JPA: @Id @GeneratedValue(strategy = GenerationType.IDENTITY)]
    # primary_key=True: PK 설정
    # index=True: 조회 성능 향상을 위한 인덱스 생성
    id = Column(Integer, primary_key=True, index=True)

    # [JPA: @Column(unique = true, length = 255)]
    email = Column(String(255), unique=True, index=True)

    # [JPA: @Column]
    hashed_password = Column(String(255))

    # [JPA: @Column(columnDefinition = "TINYINT(1) default 1")]
    is_active = Column(Boolean, default=True)
    
    # [Tip] 
    # 만약 Lombok의 @ToString 같은 게 필요하면 __repr__ 메소드를 정의하면 됩니다.
