"""Async engine + sessionmaker + FastAPI dependency."""
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from polymarket_advisor.core.config import get_settings
from polymarket_advisor.db.base import Base

_engine = None
async_session_maker = None


def init_engine() -> None:
    global _engine, async_session_maker
    settings = get_settings()
    _engine = create_async_engine(
        settings.database_url,
        echo=False,
    )
    async_session_maker = async_sessionmaker(
        _engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    if async_session_maker is None:
        init_engine()
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
