"""
Pydantic schemas for /signals.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class SignalOut(BaseModel):
    token_id: int
    score: Optional[float] = None
    edge: Optional[float] = None
    confidence: Optional[float] = None
    ts: datetime


class SignalListResponse(BaseModel):
    signals: List[SignalOut] = Field(default_factory=list)
    run_id: Optional[int] = None