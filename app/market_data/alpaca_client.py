import os

from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient


load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")


if not API_KEY or not SECRET_KEY:
    raise RuntimeError(
        "ALPACA_API_KEY and ALPACA_SECRET_KEY must be configured."
    )


client = StockHistoricalDataClient(
    api_key=API_KEY,
    secret_key=SECRET_KEY,
)