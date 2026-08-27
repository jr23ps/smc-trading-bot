from datetime import datetime

from sqlalchemy import DateTime, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Candle(Base):
    __tablename__ = "candles"

    __table_args__ = (
        UniqueConstraint(
            "symbol",
            "timeframe",
            "timestamp",
            name="uq_candle_symbol_timeframe_timestamp",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    symbol: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )

    timeframe: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        index=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    open: Mapped[float] = mapped_column(
        Numeric(12, 4),
        nullable=False,
    )

    high: Mapped[float] = mapped_column(
        Numeric(12, 4),
        nullable=False,
    )

    low: Mapped[float] = mapped_column(
        Numeric(12, 4),
        nullable=False,
    )

    close: Mapped[float] = mapped_column(
        Numeric(12, 4),
        nullable=False,
    )

    volume: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    vwap: Mapped[float | None] = mapped_column(
        Numeric(12, 4),
        nullable=True,
    )

    trade_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    def __repr__(self) -> str:
        return (
            f"<Candle "
            f"{self.symbol} "
            f"{self.timeframe} "
            f"{self.timestamp}>"
        )