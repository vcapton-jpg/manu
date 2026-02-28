"""Client Gamma API — markets/events metadata."""
import httpx
from polymarket_advisor.core.config import get_settings


class GammaClient:
    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (base_url or get_settings().polymarket_gamma_base_url).rstrip("/")

    async def get_events(self, limit: int = 100) -> list[dict]:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{self.base_url}/events", params={"limit": limit})
            r.raise_for_status()
            return r.json() if r.json() else []

    async def get_markets(self, event_slug: str | None = None) -> list[dict]:
        async with httpx.AsyncClient() as client:
            params = {}
            if event_slug:
                params["slug"] = event_slug
            r = await client.get(f"{self.base_url}/markets", params=params)
            r.raise_for_status()
            return r.json() if r.json() else []
