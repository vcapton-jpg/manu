"""Token (outcome) model."""
from sqlalchemy import String, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from polymarket_advisor.db.base import Base
from sqlalchemy import Column


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    market_id = Column(Integer, ForeignKey("markets.id", ondelete="CASCADE"), nullable=False, index=True)
    outcome = Column(String(256), nullable=True)
    token_id = Column(String(256), nullable=True, index=True)
    raw = Column(JSON, nullable=True)

    market = relationship("Market", back_populates="tokens")
    prices = relationship("Price", back_populates="token", cascade="all, delete-orphan")
    signals = relationship("Signal", back_populates="token", cascade="all, delete-orphan")
