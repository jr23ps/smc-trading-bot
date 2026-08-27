from datetime import datetime, timedelta, timezone

from app.market_data.timeframe_builder import TimeframeBuilder
from app.models.candle import Candle


def make_candles(count: int) -> list[Candle]:
    candles = []

    start = datetime(
        2026,
        8,
        26,
        9,
        0,
        tzinfo=timezone.utc,
    )

    for i in range(count):
        price = 100.0 + i

        candles.append(
            Candle(
                symbol="SPY",
                timeframe="1m",
                timestamp=start + timedelta(minutes=i),
                open=price,
                high=price + 1,
                low=price - 1,
                close=price + 0.5,
                volume=1000,
                vwap=None,
                trade_count=None,
            )
        )

    return candles


def test_build_all_timeframes():
    candles = make_candles(180)

    builder = TimeframeBuilder()

    five_minute = builder.build(candles, "5m")
    thirty_minute = builder.build(candles, "30m")
    one_hour = builder.build(candles, "1h")
    four_hour = builder.build(candles, "4h")

    assert len(five_minute) == 36
    assert len(thirty_minute) == 6
    assert len(one_hour) == 3
    assert len(four_hour) == 1