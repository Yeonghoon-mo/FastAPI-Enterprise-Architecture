from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# [Spring: application.yml] DB 연결 URL
# 형식: jdbc:mysql://localhost:3306/fastapi_db 와 동일
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1361@127.0.0.1:3306/fastapi_db"

# [Spring: DataSource] 커넥션 풀(Connection Pool) 생성
# echo=True: 실행되는 SQL을 콘솔에 출력 (Spring: spring.jpa.show-sql=true)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)

# [Spring: EntityManagerFactory] 트랜잭션 관리 및 세션 생성 공장
# 요청이 들어올 때마다 이 친구가 Session(EntityManager)을 하나씩 찍어냅니다.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# [JPA: @Entity가 상속받을 부모 클래스]
# 모든 모델(Entity)은 이 Base를 상속받아야 DB 테이블로 인식됩니다.
Base = declarative_base()

# [Spring: @Bean / DI] 의존성 주입(Dependency Injection)을 위한 함수
# Controller에서 db: Session = Depends(get_db) 로 주입받아 사용합니다.
# try-finally 구조를 통해 사용 후 반드시 close() 되도록 보장합니다. (Open Session In View 패턴과 유사)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()