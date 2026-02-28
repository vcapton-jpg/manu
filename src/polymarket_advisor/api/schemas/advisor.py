"""Pydantic schemas for /advisor."""
from pydantic import BaseModel
from typing import Any


class AdvisorOut(BaseModel):
    thesis: str
    signals: list[dict[str, Any]]
    risk_notes: str | None = None
    catalysts: list[Any] = []
    sizing: str | None = None
