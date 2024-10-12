import secrets
from datetime import date
from pathlib import Path

import pytest
from aresponses import ResponsesMockServer

from core.currency_rates_getter import CurrencyRatesGetter
from tests.fixtures import urls


@pytest.fixture
def getter() -> CurrencyRatesGetter:
    return CurrencyRatesGetter(
        currency="RUB",
    )


@pytest.fixture
def mock_currency_api_invalid_response(
    getter: CurrencyRatesGetter,
    aresponses: ResponsesMockServer,
) -> ResponsesMockServer:
    urls.mock_currencies_api(aresponses, ["foo", "bar"])
    return aresponses


@pytest.fixture
def cached_file_data(
    getter: CurrencyRatesGetter,
    mock_cache_dir_config: Path,
) -> bytes:
    request_date = date.today()
    filename = getter.get_cache_filename(
        currency=getter.source_currency,
        for_date=request_date,
    )
    filepath = mock_cache_dir_config / filename
    random_data = secrets.token_bytes(10)
    filepath.write_bytes(random_data)
    return random_data


class TestCurrencyRatesGetter:
    async def test_raises_on_not_dict_api_response(
        self,
        getter: CurrencyRatesGetter,
        mock_currency_api_invalid_response: ResponsesMockServer,
    ) -> None:
        with pytest.raises(TypeError, match="Expected API to return dict"):
            await getter.request_currency_info()
        mock_currency_api_invalid_response.assert_all_requests_matched()

    async def test_gets_from_cache(
        self,
        getter: CurrencyRatesGetter,
        cached_file_data: bytes,
    ) -> None:
        data: bytes = await getter.get_currency_info()
        assert data == cached_file_data
