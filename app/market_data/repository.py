from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.candle import Candle


class CandleRepository:
    """Handles database operations for market candles."""

    def __init__(self, session: Session):
        self.session = session

    def save_candles(self, candles: list[Candle]) -> int:
        """
        Save candles to the database.

        Returns the number of candles added.
        Existing candles are skipped.
        """

        if not candles:
            return 0

        added = 0

        for candle in candles:
            existing = self.session.scalar(
                select(Candle.id).where(
                    Candle.symbol == candle.symbol,
                    Candle.timeframe == candle.timeframe,
                    Candle.timestamp == candle.timestamp,
                )
            )

            if existing is not None:
                continue

            self.session.add(candle)
            added += 1

        self.session.commit()

        return added