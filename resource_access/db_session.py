from sqlalchemy import create_engine

sync_engine = create_engine(
    settings.postgres_url,
    pool_size=settings.sync_pool_size,
    pool_recycle=settings.sync_pool_recycle,
    max_overflow=settings.sync_max_overflow,
)
SessionLocal = sessionmaker(
    bind=sync_engine, expire_on_commit=False, class_=Session
)

async def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()