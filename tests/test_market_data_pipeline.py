from datetime import datetime, timezone

from app.market_data.pipeline import MarketDataPipeline
from app.models.candle import Candle


class FakeProvider:
    """Fake provider used for pipeline testing."""

    def get_historical_candles(
        self,
        symbol,
        timeframe,
        start,
        end,
    ):
        return [
            Candle(
                symbol=symbol,
                timeframe=timeframe,
                timestamp=start,
                open=100.0,
                high=101.0,
                low=99.0,
                close=100.5,
                volume=1000,
            )
        ]


class FakeRepository:
    """Fake repository used for pipeline testing."""

    def __init__(self):
        self.saved_candles = []

    def save_candles(self, candles):
        self.saved_candles.extend(candles)
        return len(candles)


def test_pipeline_fetches_and_stores_data():
    provider = FakeProvider()
    repository = FakeRepository()

    pipeline = MarketDataPipeline(
        provider=provider,
        repository=repository,
    )

    start = datetime(
        2026,
        8,
        26,
        14,
        30,
        tzinfo=timezone.utc,
    )

    end = datetime(
        2026,
        8,
        26,
        14,
        40,
        tzinfo=timezone.utc,
    )

    added = pipeline.run(
        symbol="SPY",
        timeframe="1m",
        start=start,
        end=end,
    )

    assert added == 1
    assert len(repository.saved_candles) == 1

    saved_candle = repository.saved_candles[0]

    assert saved_candle.symbol == "SPY"
    assert saved_candle.timeframe == "1m"
    assert saved_candle.open == 100.0
    assert saved_candle.high == 101.0
    assert saved_candle.low == 99.0
    assert saved_candle.close == 100.5
    assert saved_candle.volume == 1000