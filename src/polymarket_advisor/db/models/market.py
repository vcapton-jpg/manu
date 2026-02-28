"""Market model."""
from sqlalchemy import String, DateTime, JSON, Text
from sqlalchemy.orm import relationship
from polymarket_advisor.db.base import Base
from sqlalchemy import Column, Integer


class Market(Base):
    __tablename__ = "markets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(512), unique=True, nullable=False, index=True)
    question = Column(Text, nullable=True)
    end_date_iso = Column(String(64), nullable=True)
    raw = Column(JSON, nullable=True)

    tokens = relationship("Token", back_populates="market", cascade="all, delete-orphan")
