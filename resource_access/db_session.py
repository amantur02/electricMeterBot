from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from core.config import settings
from resource_access.db_base_class import Base

async_engine = create_async_engine(settings.postgres_url)

Base.metadata.create_all(async_engine)

AsyncSessionLocal = sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)
session = AsyncSessionLocal()
