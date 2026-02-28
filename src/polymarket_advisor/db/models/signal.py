"""Signal model — snapshot row: (signal_run_id, token_id)."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship

from polymarket_advisor.db.base import Base


class Signal(Base):
    __tablename__ = "signals"

    # ✅ snapshot-safe primary key
    signal_run_id = Column(
        Integer,
        ForeignKey("signal_runs.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
        nullable=False,
    )
    token_id = Column(
        Integer,
        ForeignKey("tokens.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
        nullable=False,
    )

    score = Column(Numeric(10, 4), nullable=True)
    edge = Column(Numeric(10, 4), nullable=True)
    confidence = Column(Numeric(10, 4), nullable=True)

    # This must be constant within one run (we set it to SignalRun.run_ts)
    ts = Column(DateTime(timezone=True), nullable=False, index=True)

    signal_run = relationship("SignalRun", back_populates="signals")
    token = relationship("Token", back_populates="signals")