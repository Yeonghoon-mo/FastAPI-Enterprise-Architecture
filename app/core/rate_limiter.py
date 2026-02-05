from fastapi import Request, HTTPException, status
import time
from app.core.redis import redis_client
from app.core.logger import logger

class RateLimiter:
    """
    Redis를 사용한 Sliding Window Rate Limiter
    """
    def __init__(self, times: int = 10, seconds: int = 60):
        self.times = times
        self.seconds = seconds

    async def __call__(self, request: Request):
        # 1. 클라이언트 식별자 결정 (로그인 유저 우선, 없으면 IP)
        user = getattr(request.state, "user", None)
        if user:
            identifier = f"user:{user.id}"
        else:
            # Nginx 등을 거칠 경우 X-Forwarded-For 고려 가능
            identifier = f"ip:{request.client.host}"

        # 2. Redis Key 생성 (API 경로별로 별도 카운트)
        path = request.url.path
        key = f"ratelimit:{identifier}:{path}"

        # 3. Sliding Window 로직 (Lua 스크립트 사용으로 원자성 보장)
        current_time = time.time()
        window_start = current_time - self.seconds

        # Lua 스크립트: 
        # 1. 윈도우 밖의 데이터 삭제 (ZREMRANGEBYSCORE)
        # 2. 현재 요청 수 확인 (ZCARD)
        # 3. 제한 이내면 현재 요청 추가 (ZADD) 및 만료시간 설정
        lua_script = """
        local key = KEYS[1]
        local limit = tonumber(ARGV[1])
        local window = tonumber(ARGV[2])
        local current_time = tonumber(ARGV[3])
        local window_start = tonumber(ARGV[4])

        redis.call('ZREMRANGEBYSCORE', key, 0, window_start)
        local current_count = redis.call('ZCARD', key)

        if current_count < limit then
            redis.call('ZADD', key, current_time, current_time)
            redis.call('EXPIRE', key, window)
            return {1, current_count + 1}
        else
            return {0, current_count}
        end
        """

        result = await redis_client.eval(
            lua_script, 
            1, 
            key, 
            self.times, 
            self.seconds, 
            current_time, 
            window_start
        )

        allowed, count = result[0], result[1]

        if not allowed:
            logger.warning(f"Rate limit exceeded for {identifier} on {path} ({count}/{self.times})")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {self.times} requests per {self.seconds} seconds."
            )

        return True
