from datetime import datetime, timedelta, timezone

from app.database.session import SessionLocal
from app.market_data.alpaca_provider import AlpacaDataProvider
from app.market_data.pipeline import MarketDataPipeline
from app.market_data.repository import CandleRepository


def main():
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=10)

    session = SessionLocal()

    try:
        provider = AlpacaDataProvider()
        repository = CandleRepository(session)

        pipeline = MarketDataPipeline(
            provider=provider,
            repository=repository,
        )

        added = pipeline.run(
            symbol="SPY",
            timeframe="1m",
            start=start,
            end=end,
        )

        print(f"Fetched and stored {added} new candles.")

    finally:
        session.close()


if __name__ == "__main__":
    main()