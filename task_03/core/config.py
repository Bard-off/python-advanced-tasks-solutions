import logging
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "currencies-data-cache"

CURRENCIES_LIST_API_URL = (
    "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api"
    "@latest/v1/currencies.json"
)
CURRENCY_API_URL = (
    "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api"
    "@{date}/v1/currencies/{currency}.json"
)

TARGET_CURRENCIES = (
    "rub",
    "usd",
    "eur",
    "inr",
    "jpy",
)


DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)s:%(lineno)d %(levelname)s - %(message)s"
)


def configure_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format=DEFAULT_FORMAT,
    )
