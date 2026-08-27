from datetime import datetime, timedelta, timezone

from app.database.session import SessionLocal
from app.market_data.alpaca_provider import AlpacaDataProvider
from app.market_data.repository import CandleRepository


provider = AlpacaDataProvider()

end = datetime.now(timezone.utc)
start = end - timedelta(minutes=10)

candles = provider.get_historical_candles(
    symbol="SPY",
    timeframe="1m",
    start=start,
    end=end,
)

session = SessionLocal()

try:
    repository = CandleRepository(session)

    added = repository.save_candles(candles)

    print(f"Received: {len(candles)} candles")
    print(f"Added to database: {added} candles")

finally:
    session.close()