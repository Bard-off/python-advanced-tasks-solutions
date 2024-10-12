import datetime
import random
from pathlib import Path
from typing import Any
from unittest import mock

import pytest
from _pytest.fixtures import SubRequest
from aiohttp.test_utils import TestClient
from aresponses import ResponsesMockServer

from app import create_app
from core.config import TARGET_CURRENCIES, configure_logging
from tests.fixtures import urls

configure_logging()


# fix for aiohttp_client + aresponses
# https://github.com/aresponses/aresponses#:~:text=If%20you%27re%20trying%20to%20use%20the%20aiohttp_client%20test%20fixture
@pytest.fixture
def loop(event_loop):
    """replace aiohttp loop fixture with pytest-asyncio fixture"""
    return event_loop


# working with pytest-aiohttp
# If you need to use aresponses together with pytest-aiohttp, you should re-initialize the main aresponses fixture with the loop fixture
# https://github.com/aresponses/aresponses#:~:text=If%20you%20need%20to%20use%20aresponses%20together%20with%20pytest%2Daiohttp
@pytest.fixture
async def aresponses(loop) -> ResponsesMockServer:
    async with ResponsesMockServer(loop=loop) as server:
        # allow all local requests - required for web app testing
        server.add_local_passthrough()
        yield server


@pytest.fixture
async def client(aiohttp_client) -> TestClient:
    return await aiohttp_client(create_app())


@pytest.fixture
def mock_currencies_list_response(
    aresponses: ResponsesMockServer,
) -> dict[str, str]:
    return urls.mock_list_currencies(aresponses)


@pytest.fixture
def mock_currency_api_response(
    request: SubRequest,
    aresponses: ResponsesMockServer,
) -> tuple[str, dict[str, Any]]:
    date_str: str = datetime.date.today().isoformat()
    param = request.param
    if isinstance(param, str):
        currency = param
    else:
        currency, date_str = param
    currency = currency.lower()
    currencies_data = {
        # just some random positive value
        cur: random.random()
        # we need only those declared in config
        for cur in TARGET_CURRENCIES
    }
    currencies_data[currency] = 1
    prepared_response = {
        "date": date_str,
        currency: currencies_data,
    }

    urls.mock_currencies_api(aresponses, prepared_response)
    return (
        currency,
        prepared_response,
    )


@pytest.fixture(autouse=True)
def mock_cache_dir_config(tmp_path: Path) -> Path:
    with mock.patch(
        "core.currency_rates_getter.CACHE_DIR",
        tmp_path,
    ):
        yield tmp_path
