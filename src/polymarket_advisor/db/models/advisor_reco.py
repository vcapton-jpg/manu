"""Advisor recommendation model."""
from sqlalchemy import String, DateTime, Text, JSON
from polymarket_advisor.db.base import Base
from sqlalchemy import Column, Integer


class AdvisorReco(Base):
    __tablename__ = "advisor_recos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    run_ts = Column(DateTime(timezone=True), nullable=False, index=True)
    profile = Column(String(64), nullable=True)
    payload = Column(JSON, nullable=True)
    thesis = Column(Text, nullable=True)
    risk_notes = Column(Text, nullable=True)
