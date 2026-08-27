from datetime import datetime, timedelta


TIMEFRAME_MINUTES = {
    "1m": 1,
    "5m": 5,
    "30m": 30,
    "1h": 60,
    "4h": 240,
}


class CandleCompletion:
    """Determines whether a candle has completely closed."""

    @staticmethod
    def is_closed(
        timestamp: datetime,
        timeframe: str,
        current_time: datetime,
    ) -> bool:
        """
        Return True when the candle's timeframe has finished.

        The timestamp represents the beginning of the candle.
        """

        if timeframe not in TIMEFRAME_MINUTES:
            raise ValueError(
                f"Unsupported timeframe: {timeframe}"
            )

        duration = timedelta(
            minutes=TIMEFRAME_MINUTES[timeframe]
        )

        candle_end = timestamp + duration

        return current_time >= candle_end