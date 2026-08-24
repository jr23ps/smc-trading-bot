from datetime import datetime, timezone

from app.database.session import SessionLocal
from app.models import Candle


def test_create_and_read_candle():
    session = SessionLocal()

    try:
        candle = Candle(
            symbol="MES",
            timeframe="1m",
            timestamp=datetime(
                2026,
                8,
                24,
                14,
                30,
                tzinfo=timezone.utc,
            ),
            open=6500.00,
            high=6503.00,
            low=6499.50,
            close=6502.25,
            volume=1842,
        )

        session.add(candle)
        session.commit()
        session.refresh(candle)

        assert candle.id is not None

        saved_candle = session.get(Candle, candle.id)

        assert saved_candle is not None
        assert saved_candle.symbol == "MES"
        assert saved_candle.timeframe == "1m"
        assert saved_candle.open == 6500.00
        assert saved_candle.high == 6503.00
        assert saved_candle.low == 6499.50
        assert saved_candle.close == 6502.25
        assert saved_candle.volume == 1842

    finally:
        session.close()