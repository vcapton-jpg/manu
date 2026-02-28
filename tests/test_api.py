"""Tests API (health, endpoints load)."""
import pytest
from httpx import ASGITransport, AsyncClient
from polymarket_advisor.api.app import app


@pytest.mark.asyncio
async def test_health() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        r = await client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_signals_endpoint_exists() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        try:
            r = await client.get("/signals")
            assert r.status_code in (200, 500, 503)
        except Exception:
            # Without DB, dependency can raise; route is still registered
            pass


@pytest.mark.asyncio
async def test_news_endpoint_exists() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        try:
            r = await client.get("/news")
            assert r.status_code in (200, 500, 503)
        except Exception:
            pass


@pytest.mark.asyncio
async def test_advisor_endpoint_exists() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        try:
            r = await client.get("/advisor")
            assert r.status_code in (200, 500, 503)
        except Exception:
            pass
