"""Client RSS pour actualités."""
import httpx


class RssClient:
    def __init__(self, feed_url: str) -> None:
        self.feed_url = feed_url

    async def fetch(self) -> list[dict]:
        async with httpx.AsyncClient() as client:
            r = await client.get(self.feed_url)
            r.raise_for_status()
            # Placeholder: parser XML RSS -> list[dict]
            return []
