"""Pydantic schemas for /news."""
from pydantic import BaseModel
from datetime import datetime


class NewsOut(BaseModel):
    id: int
    title: str | None
    url: str | None
    source: str | None
    published_at: datetime | None

    model_config = {"from_attributes": True}


class NewsListResponse(BaseModel):
    news: list[NewsOut]
