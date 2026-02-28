"""Signal run (batch) model — one row per snapshot."""
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import relationship

from polymarket_advisor.db.base import Base


class SignalRun(Base):
    __tablename__ = "signal_runs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    run_ts = Column(DateTime(timezone=True), nullable=False, index=True)

    signals = relationship(
        "Signal",
        back_populates="signal_run",
        cascade="all, delete-orphan",
    )