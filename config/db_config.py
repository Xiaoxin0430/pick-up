import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / "static" / ".env")

# 数据库URL
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")
if not ASYNC_DATABASE_URL:
    raise RuntimeError("ASYNC_DATABASE_URL is not configured in static/.env")
# 数据库引擎
create_table_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=2
)
# 异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=create_table_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
# 创建依赖项
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
