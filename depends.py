from sqlalchemy.orm import Session

from resource_access.db_session import AsyncSessionLocal


async def get_session() -> Session:
    session = AsyncSessionLocal()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()