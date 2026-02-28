"""Pytest fixtures."""
import pytest
from httpx import ASGITransport, AsyncClient
from polymarket_advisor.api.app import app


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def client() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
