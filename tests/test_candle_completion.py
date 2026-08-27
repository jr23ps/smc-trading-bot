from datetime import datetime, timezone

from app.market_data.candle_completion import CandleCompletion


def test_candle_is_not_closed_before_end_time():
    candle_time = datetime(
        2026,
        8,
        26,
        10,
        30,
        tzinfo=timezone.utc,
    )

    before_close = datetime(
        2026,
        8,
        26,
        10,
        34,
        59,
        tzinfo=timezone.utc,
    )

    assert (
        CandleCompletion.is_closed(
            candle_time,
            "5m",
            before_close,
        )
        is False
    )


def test_candle_is_closed_at_end_time():
    candle_time = datetime(
        2026,
        8,
        26,
        10,
        30,
        tzinfo=timezone.utc,
    )

    at_close = datetime(
        2026,
        8,
        26,
        10,
        35,
        tzinfo=timezone.utc,
    )

    assert (
        CandleCompletion.is_closed(
            candle_time,
            "5m",
            at_close,
        )
        is True
    )


def test_candle_is_closed_after_end_time():
    candle_time = datetime(
        2026,
        8,
        26,
        10,
        30,
        tzinfo=timezone.utc,
    )

    after_close = datetime(
        2026,
        8,
        26,
        10,
        36,
        tzinfo=timezone.utc,
    )

    assert (
        CandleCompletion.is_closed(
            candle_time,
            "5m",
            after_close,
        )
        is True
    )