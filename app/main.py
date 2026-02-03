from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from contextlib import asynccontextmanager
from app.routers import user_router, auth_router, board_router, comment_router
from app.core.database import engine, Base
from app.core.logger import setup_logger
from app.core.config import settings
from app.core.redis import close_redis_connection
import os

# 로거 설정 초기화
logger = setup_logger()

# 비동기 DB 초기화 (Startup Event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: DB 테이블 생성
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 업로드 디렉토리 생성
    if not os.path.exists(settings.UPLOAD_DIR):
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    yield
    
    # Shutdown
    await close_redis_connection()

app = FastAPI(
    title="FastAPI MariaDB CRUD",
    description="Spring 개발자를 위한 FastAPI CRUD 예제 프로젝트",
    version="0.0.1",
    lifespan=lifespan
)

# 정적 파일 서버 설정 (프로필 이미지 등)
app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")

# 라우터 등록
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(board_router.router)
app.include_router(comment_router.router)

@app.get("/")
async def root():
    logger.info("Root endpoint called!") # 색깔 있는 로그 출력!
    return {"message": "Hello World! FastAPI is running (Async Mode)! 🚀"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)