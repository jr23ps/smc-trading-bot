from datetime import datetime

from app.market_data.provider import MarketDataProvider
from app.market_data.repository import CandleRepository


class MarketDataService:
    """Coordinates market-data retrieval and storage."""

    def __init__(
        self,
        provider: MarketDataProvider,
        repository: CandleRepository,
    ):
        self.provider = provider
        self.repository = repository

    def fetch_and_store(
        self,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
    ) -> int:
        """
        Fetch candles from the configured provider
        and store them in the database.

        Returns the number of newly stored candles.
        """

        candles = self.provider.get_historical_candles(
            symbol=symbol,
            timeframe=timeframe,
            start=start,
            end=end,
        )

        if not candles:
            return 0

        return self.repository.save_candles(candles)