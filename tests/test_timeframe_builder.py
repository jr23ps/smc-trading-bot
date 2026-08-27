from datetime import datetime, timezone

from app.market_data.timeframe_builder import TimeframeBuilder
from app.models.candle import Candle


def make_candle(
    minute: int,
    open_price: float,
    high: float,
    low: float,
    close: float,
    volume: int,
) -> Candle:
    return Candle(
        symbol="SPY",
        timeframe="1m",
        timestamp=datetime(
            2026,
            8,
            26,
            9,
            minute,
            tzinfo=timezone.utc,
        ),
        open=open_price,
        high=high,
        low=low,
        close=close,
        volume=volume,
        vwap=None,
        trade_count=None,
    )


def test_build_five_minute_candle():
    candles = [
        make_candle(30, 100.0, 101.0, 99.5, 100.5, 1000),
        make_candle(31, 100.5, 102.0, 100.0, 101.5, 1100),
        make_candle(32, 101.5, 103.0, 101.0, 102.5, 1200),
        make_candle(33, 102.5, 104.0, 102.0, 103.5, 1300),
        make_candle(34, 103.5, 105.0, 103.0, 104.5, 1400),
    ]

    builder = TimeframeBuilder()

    five_minute = builder.build(
        candles,
        "5m",
    )

    assert len(five_minute) == 1

    candle = five_minute[0]

    assert candle.symbol == "SPY"
    assert candle.timeframe == "5m"
    assert candle.open == 100.0
    assert candle.high == 105.0
    assert candle.low == 99.5
    assert candle.close == 104.5
    assert candle.volume == 6000