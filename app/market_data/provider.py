from abc import ABC, abstractmethod
from datetime import datetime

from app.models.candle import Candle


class MarketDataProvider(ABC):
    """
    Interface for market-data providers.

    Any provider we use in the future must implement
    the methods defined here.
    """

    @abstractmethod
    def get_historical_candles(
        self,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
    ) -> list[Candle]:
        """
        Return historical candles for a symbol and timeframe.
        """
        raise NotImplementedError