from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

async_engine = create_async_engine(settings.postgres_async_url, echo=True, future=True)
async_engine.dialect.driver = "asyncpg"

AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)
session = AsyncSessionLocal()
