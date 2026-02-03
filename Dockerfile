# Python 3.10 slim 버전 사용 (가벼움)
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치 (필요한 경우)
RUN apt-get update && apt-get install -y gcc default-libmysqlclient-dev && rm -rf /var/lib/apt/lists/*

# 패키지 목록 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# Celery Worker 실행 커맨드 (루트에서 실행)
# app.core.celery_app 모듈의 celery_app 객체 실행
CMD ["celery", "-A", "app.core.celery_app", "worker", "--loglevel=info"]
