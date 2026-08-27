from datetime import datetime, timedelta, timezone

from app.market_data.alpaca_provider import AlpacaDataProvider


provider = AlpacaDataProvider()

end = datetime.now(timezone.utc)
start = end - timedelta(minutes=10)

candles = provider.get_historical_candles(
    symbol="SPY",
    timeframe="1m",
    start=start,
    end=end,
)

print(f"Received {len(candles)} candles")

for candle in candles:
    print(
        candle.timestamp,
        candle.open,
        candle.high,
        candle.low,
        candle.close,
        candle.volume,
    )