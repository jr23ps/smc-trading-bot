from datetime import datetime

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Candle(Base):
    __tablename__ = "candles"

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

    def __repr__(self) -> str:
        return (
            f"<Candle "
            f"{self.symbol} "
            f"{self.timeframe} "
            f"{self.timestamp}>"
        )