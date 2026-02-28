"""News item model."""
from sqlalchemy import String, DateTime, Text, JSON
from polymarket_advisor.db.base import Base
from sqlalchemy import Column, Integer


class NewsItem(Base):
    __tablename__ = "news_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=True)
    url = Column(String(2048), nullable=True)
    source = Column(String(256), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True, index=True)
    raw = Column(JSON, nullable=True)
