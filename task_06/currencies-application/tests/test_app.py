from dataclasses import asdict
from datetime import date, timedelta
from http import HTTPStatus
from typing import Any

import pytest
from aiohttp.test_utils import TestClient

from core.currency_rates_getter import CurrencyRatesGetter
from helpers.request_param_reader import (
    INVALID_DATE_MESSAGE,
    UNKNOWN_CURRENCY_MESSAGE_TEMPLATE,
)


class TestGetCurrencyRates:

    @classmethod
    def prepare_expected_response_data(
        cls,
        currency: str,
        api_response_data: dict[str, Any],
    ) -> dict[str, Any]:
        getter = CurrencyRatesGetter(currency=currency)
        currency_info = getter.prepare_currency_info_from_response_data(
            response_data=api_response_data,
        )
        expected_data = asdict(currency_info)
        expected_data["date"] = currency_info.date.isoformat()
        for currency_value in expected_data["values"]:
            # convert decimal to string
            currency_value["value"] = str(currency_value["value"])
        return expected_data

    @pytest.mark.parametrize(
        "mock_currency_api_response",
        [
            "RUB",
            "EUR",
            pytest.param(("RUB", date.today().isoformat()), id="rub-for-today"),
            pytest.param(
                ("RUB", (date.today() - timedelta(days=10)).isoformat()),
                id="rub-for-prev-day",
            ),
        ],
        indirect=True,
    )
    async def test_success(
        self,
        client: TestClient,
        mock_currency_api_response: tuple[str, dict[str, Any]],
        mock_currencies_list_response: dict[str, str],
    ) -> None:
        currency, api_response_data = mock_currency_api_response
        response = await client.get(f"/rates/{currency}")
        assert response.status == HTTPStatus.OK, await response.text()
        response_data = await response.json()
        expected_data = self.prepare_expected_response_data(
            currency=currency,
            api_response_data=api_response_data,
        )
        assert response_data == expected_data

    async def test_get_invalid_currency(
        self,
        client: TestClient,
        mock_currencies_list_response: dict[str, str],
    ) -> None:
        invalid_currency = "some-invalid-currency"
        # assert invalid_currency not in mock_currencies_list_response
        response = await client.get(f"/rates/{invalid_currency}")
        assert response.status == HTTPStatus.NOT_FOUND, await response.text()
        response_data = await response.json()
        expected_data = {
            "message": UNKNOWN_CURRENCY_MESSAGE_TEMPLATE.format(
                currency=invalid_currency,
            )
        }
        assert response_data == expected_data

    async def test_get_invalid_date(
        self,
        client: TestClient,
        mock_currencies_list_response: dict[str, str],
    ):
        invalid_date = "2020-15-33"
        response = await client.get(f"/rates/rub/{invalid_date}")
        assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY, await response.text()
        response_data = await response.json()
        expected_data = {"message": INVALID_DATE_MESSAGE}
        assert response_data == expected_data
