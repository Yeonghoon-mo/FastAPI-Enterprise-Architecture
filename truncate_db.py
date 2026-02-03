import asyncio
from sqlalchemy import text
from app.core.database import engine, Base
# 모델을 임포트해야 Base.metadata에 테이블 정보가 등록됨
from app.models import user, board, comment

async def truncate_all_tables():
    async with engine.begin() as conn:
        print("🔄 Truncating all tables...")
        await conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        
        # 순서대로 Truncate (혹은 모든 테이블)
        for table in reversed(Base.metadata.sorted_tables):
            print(f"🗑 Truncating table: {table.name}")
            await conn.execute(text(f"TRUNCATE TABLE {table.name};"))
            
        await conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        print("✅ All tables truncated successfully.")

if __name__ == "__main__":
    asyncio.run(truncate_all_tables())
