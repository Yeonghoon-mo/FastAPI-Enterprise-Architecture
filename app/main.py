from fastapi import FastAPI
import uvicorn
from app.routers import user_router, auth_router, board_router, comment_router
from app.core.database import engine, Base
from app.core.logger import setup_logger

# 로거 설정 초기화
logger = setup_logger()

# DB 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI MariaDB CRUD",
    description="Spring 개발자를 위한 FastAPI CRUD 예제 프로젝트",
    version="0.0.1"
)

# 라우터 등록
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(board_router.router)
app.include_router(comment_router.router)

@app.get("/")
def root():
    logger.info("Root endpoint called!") # 색깔 있는 로그 출력!
    return {"message": "Hello World! FastAPI is running! 🚀"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

