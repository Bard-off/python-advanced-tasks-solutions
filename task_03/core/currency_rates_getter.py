from dataclasses import asdict
from datetime import date
from typing import Iterable

import aiofiles
import aiohttp

from core.config import CACHE_DIR, CURRENCY_API_URL, TARGET_CURRENCIES
from core.types import CurrencyInfo, ResponseType
from helpers.json_coders import json_decoder_decimal, json_encoder


class CurrencyRatesGetter:
    def __init__(
        self,
        currency: str,
        to_currencies: Iterable[str] = TARGET_CURRENCIES,
        for_date: date | None = None,
    ) -> None:
        self.source_currency = currency.lower()
        self.target_currencies = {cur.lower() for cur in to_currencies}
        self.for_date: date = for_date or date.today()
        self.selected_date = self.for_date.isoformat()

    @classmethod
    def get_cache_filename(
        cls,
        currency: str,
        for_date: date,
    ) -> str:
        return f"{for_date.isoformat()}-{currency}.json"

    async def request_currency_info(
        self,
    ) -> ResponseType:
        url = CURRENCY_API_URL.format(
            date=self.selected_date,
            currency=self.source_currency,
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.json(loads=json_decoder_decimal.decode)

    async def read_currency_info_for_date(
        self,
    ) -> CurrencyInfo:
        data = await self.request_currency_info()
        info = CurrencyInfo.from_currency_info_response(
            info=data,
            source_currency=self.source_currency,
            target_currencies=self.target_currencies,
        )
        return info

    @classmethod
    async def save_cached_currency_info(
        cls,
        info: CurrencyInfo,
    ) -> bytes:
        filename = cls.get_cache_filename(
            currency=info.currency,
            for_date=info.date,
        )

        filepath = CACHE_DIR / filename
        info_data_bytes = json_encoder.encode(asdict(info)).encode("utf-8")
        async with aiofiles.open(filepath, "wb") as f:
            await f.write(info_data_bytes)

        return info_data_bytes

    async def read_and_save_currency_info(self) -> bytes:
        info = await self.read_currency_info_for_date()
        info_data_bytes = await self.save_cached_currency_info(info)
        return info_data_bytes

    async def read_currency_info_from_cache(self) -> bytes | None:
        filename = self.get_cache_filename(
            currency=self.source_currency,
            for_date=self.for_date,
        )
        filepath = CACHE_DIR / filename
        if filepath.exists():
            async with aiofiles.open(filepath, mode="rb") as file:
                return await file.read()

    async def get_currency_info(self) -> bytes:
        cached = await self.read_currency_info_from_cache()
        if cached is not None:
            return cached

        return await self.read_and_save_currency_info()
