from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. DB 연결 URL 설정 (Spring의 application.yml 역할)
# 형식: mysql+pymysql://<username>:<password>@<host>:<port>/<db_name>
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1361@127.0.0.1:3306/fastapi_db"

# 2. Engine 생성 (Connection Pool 생성)
# echo=True 옵션은 실행되는 SQL을 로그로 보여줍니다 (Spring의 show-sql: true)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)

# 3. SessionLocal 생성 (JPA EntityManagerFactory 역할)
# 요청마다 이 클래스를 통해 DB 세션을 생성합니다.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base 클래스 (Entity들이 상속받을 부모 클래스)
Base = declarative_base()

# 5. Dependency Injection용 함수 (Controller에서 사용)
# 요청이 들어오면 DB 세션을 열고, 처리가 끝나면 닫아줍니다.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
