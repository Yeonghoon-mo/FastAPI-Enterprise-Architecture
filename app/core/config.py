from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# 프로젝트 루트 경로 찾기 (app/core/config.py 기준 -> app/core -> app -> root)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    # Database
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Uploads
    UPLOAD_DIR: str = "static/uploads"

    # DB URL 자동 생성
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    # .env 파일 로드 설정 (절대 경로 사용)
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH), 
        env_file_encoding="utf-8",
        extra="ignore" # .env에 정의되지 않은 환경변수가 있어도 무시 (에러 방지)
    )

# 전역 설정 객체 (Singleton처럼 사용)
settings = Settings()
