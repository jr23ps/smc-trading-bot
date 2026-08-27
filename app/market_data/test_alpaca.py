from datetime import datetime, timedelta, timezone

from alpaca.data.enums import DataFeed
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from app.market_data.alpaca_client import client


end = datetime.now(timezone.utc)
start = end - timedelta(minutes=10)

request = StockBarsRequest(
    symbol_or_symbols="SPY",
    timeframe=TimeFrame.Minute,
    start=start,
    end=end,
    feed=DataFeed.IEX,
)


bars = client.get_stock_bars(request)


print(bars)