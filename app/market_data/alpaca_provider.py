from datetime import datetime

from alpaca.data.enums import DataFeed
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from app.market_data.alpaca_client import client
from app.market_data.provider import MarketDataProvider
from app.models.candle import Candle


class AlpacaDataProvider(MarketDataProvider):

    def get_historical_candles(
        self,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
    ) -> list[Candle]:

        if timeframe != "1m":
            raise ValueError(
                "AlpacaDataProvider currently supports only 1m candles."
            )

        request = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=TimeFrame.Minute,
            start=start,
            end=end,
            feed=DataFeed.IEX,
        )

        bars = client.get_stock_bars(request)

        candles = []

        symbol_bars = bars.data.get(symbol, [])

        for bar in symbol_bars:
            candle = Candle(
                symbol=bar.symbol,
                timeframe=timeframe,
                timestamp=bar.timestamp,
                open=bar.open,
                high=bar.high,
                low=bar.low,
                close=bar.close,
                volume=int(bar.volume),
                vwap=bar.vwap,
                trade_count=int(bar.trade_count),
            )

            candles.append(candle)

        return candles