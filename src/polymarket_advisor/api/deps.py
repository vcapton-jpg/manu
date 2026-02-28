"""FastAPI dependencies: get_db_session, auth if any."""
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from polymarket_advisor.db.session import get_db, async_session_maker
from polymarket_advisor.db import init_engine


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    if async_session_maker is None:
        init_engine()
    async for session in get_db():
        yield session
