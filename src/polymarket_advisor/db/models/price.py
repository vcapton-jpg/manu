"""Price snapshot model."""
from sqlalchemy import Numeric, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from polymarket_advisor.db.base import Base
from sqlalchemy import Column


class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token_id = Column(Integer, ForeignKey("tokens.id", ondelete="CASCADE"), nullable=False, index=True)
    price = Column(Numeric(10, 4), nullable=True)
    ts = Column(DateTime(timezone=True), nullable=False, index=True)

    token = relationship("Token", back_populates="prices")
