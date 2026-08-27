from datetime import datetime, timedelta

from app.models.candle import Candle


class TimeframeBuilder:
    """Build higher-timeframe candles from 1-minute candles."""

    TIMEFRAME_MINUTES = {
        "1m": 1,
        "5m": 5,
        "30m": 30,
        "1h": 60,
        "4h": 240,
    }

    def build(
        self,
        candles: list[Candle],
        timeframe: str,
    ) -> list[Candle]:
        """
        Build candles for the requested timeframe.

        Input candles must be 1-minute candles.
        """

        if timeframe not in self.TIMEFRAME_MINUTES:
            raise ValueError(
                f"Unsupported timeframe: {timeframe}"
            )

        if not candles:
            return []

        if timeframe == "1m":
            return candles.copy()

        minutes = self.TIMEFRAME_MINUTES[timeframe]

        candles = sorted(
            candles,
            key=lambda candle: candle.timestamp,
        )

        result = []

        current_group = []
        current_start = None

        for candle in candles:
            bucket_start = self._get_bucket_start(
                candle.timestamp,
                minutes,
            )

            if current_start is None:
                current_start = bucket_start

            if bucket_start != current_start:
                result.append(
                    self._combine(
                        current_group,
                        current_start,
                        timeframe,
                    )
                )

                current_group = []
                current_start = bucket_start

            current_group.append(candle)

        if current_group:
            result.append(
                self._combine(
                    current_group,
                    current_start,
                    timeframe,
                )
            )

        return result

    @staticmethod
    def _get_bucket_start(
        timestamp: datetime,
        minutes: int,
    ) -> datetime:
        """Return the beginning of the timeframe bucket."""

        total_minutes = timestamp.hour * 60 + timestamp.minute

        bucket_minutes = (
            total_minutes // minutes
        ) * minutes

        hour = bucket_minutes // 60
        minute = bucket_minutes % 60

        return timestamp.replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0,
        )

    @staticmethod
    def _combine(
        candles: list[Candle],
        timestamp: datetime,
        timeframe: str,
    ) -> Candle:
        """Combine multiple candles into one candle."""

        first = candles[0]
        last = candles[-1]

        return Candle(
            symbol=first.symbol,
            timeframe=timeframe,
            timestamp=timestamp,
            open=first.open,
            high=max(c.high for c in candles),
            low=min(c.low for c in candles),
            close=last.close,
            volume=sum(c.volume for c in candles),
            vwap=None,
            trade_count=None,
        )