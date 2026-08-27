from datetime import datetime, timezone

import pytest

from app.market_data.service import MarketDataService
from app.models.candle import Candle


class FakeProvider:
    """Fake market-data provider for testing."""

    def __init__(self, candles):
        self.candles = candles

    def get_historical_candles(
        self,
        symbol,
        timeframe,
        start,
        end,
    ):
        return self.candles


class FakeRepository:
    """Fake repository for testing."""

    def __init__(self):
        self.saved_candles = []

    def save_candles(self, candles):
        self.saved_candles.extend(candles)
        return len(candles)


def test_market_data_service_fetches_and_stores_candles():
    candle = Candle(
        symbol="SPY",
        timeframe="1m",
        timestamp=datetime(
            2026,
            8,
            26,
            14,
            30,
            tzinfo=timezone.utc,
        ),
        open=100.0,
        high=101.0,
        low=99.0,
        close=100.5,
        volume=1000,
    )

    provider = FakeProvider([candle])
    repository = FakeRepository()

    service = MarketDataService(
        provider=provider,
        repository=repository,
    )

    added = service.fetch_and_store(
        symbol="SPY",
        timeframe="1m",
        start=datetime(
            2026,
            8,
            26,
            14,
            30,
            tzinfo=timezone.utc,
        ),
        end=datetime(
            2026,
            8,
            26,
            14,
            40,
            tzinfo=timezone.utc,
        ),
    )

    assert added == 1
    assert len(repository.saved_candles) == 1
    assert repository.saved_candles[0].symbol == "SPY"


def test_market_data_service_handles_no_candles():
    provider = FakeProvider([])
    repository = FakeRepository()

    service = MarketDataService(
        provider=provider,
        repository=repository,
    )

    added = service.fetch_and_store(
        symbol="SPY",
        timeframe="1m",
        start=datetime(
            2026,
            8,
            26,
            14,
            30,
            tzinfo=timezone.utc,
        ),
        end=datetime(
            2026,
            8,
            26,
            14,
            40,
            tzinfo=timezone.utc,
        ),
    )

    assert added == 0
    assert repository.saved_candles == []


def test_market_data_service_propagates_provider_error():
    class FailingProvider:
        def get_historical_candles(
            self,
            symbol,
            timeframe,
            start,
            end,
        ):
            raise RuntimeError("Market data provider failed")

    repository = FakeRepository()

    service = MarketDataService(
        provider=FailingProvider(),
        repository=repository,
    )

    with pytest.raises(
        RuntimeError,
        match="Market data provider failed",
    ):
        service.fetch_and_store(
            symbol="SPY",
            timeframe="1m",
            start=datetime(
                2026,
                8,
                26,
                14,
                30,
                tzinfo=timezone.utc,
            ),
            end=datetime(
                2026,
                8,
                26,
                14,
                40,
                tzinfo=timezone.utc,
            ),
        )