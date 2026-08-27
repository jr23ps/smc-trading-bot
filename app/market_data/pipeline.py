from datetime import datetime

from app.market_data.provider import MarketDataProvider
from app.market_data.repository import CandleRepository
from app.market_data.service import MarketDataService


class MarketDataPipeline:
    """Fetches market data and stores it in PostgreSQL."""

    def __init__(
        self,
        provider: MarketDataProvider,
        repository: CandleRepository,
    ):
        self.provider = provider
        self.repository = repository

        self.service = MarketDataService(
            provider=self.provider,
            repository=self.repository,
        )

    def run(
        self,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
    ) -> int:
        """
        Fetch market data and store it.

        Returns the number of newly stored candles.
        """

        return self.service.fetch_and_store(
            symbol=symbol,
            timeframe=timeframe,
            start=start,
            end=end,
        )