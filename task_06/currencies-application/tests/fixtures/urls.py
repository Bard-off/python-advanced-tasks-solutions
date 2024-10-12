import re
from typing import Any

from aresponses import ResponsesMockServer

from core import config
from tests.utils.urls import extract_host_and_path
from .currencies_api_data import KNOWN_CURRENCIES


def mock_list_currencies(
    aresponses: ResponsesMockServer,
) -> dict[str, str]:
    host, path = extract_host_and_path(config.CURRENCIES_LIST_API_URL)
    aresponses.add(host, path, "GET", response=KNOWN_CURRENCIES)
    return KNOWN_CURRENCIES


def mock_currencies_api(
    aresponses: ResponsesMockServer,
    response_data: dict[str, Any] | Any,
) -> dict[str, Any]:
    host, path = extract_host_and_path(config.CURRENCY_API_URL)
    # Captures either an ISO date or the literal string "latest" in a named group called date:
    date_pattern = r"(?P<date>(\d{4}-\d{2}-\d{2}|latest))"
    # Captures the currency in a named group called currency
    currency_pattern = r"(?P<currency>[a-z]+)"
    regex_path = path.format(
        date=date_pattern,
        currency=currency_pattern,
    ).replace(r".json", r"\.json")
    aresponses.add(host, re.compile(regex_path), "GET", response=response_data)
    return response_data
