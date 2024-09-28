import logging
from dataclasses import dataclass, field

import aiohttp

from core import config

log = logging.getLogger(__name__)


@dataclass
class CurrencyExistsCheck:
    cached_currencies: set[str] = field(default_factory=set)

    @classmethod
    async def get_all_currencies(cls) -> set[str]:
        log.info("Fetch all currencies")
        async with aiohttp.ClientSession() as session:
            async with session.get(config.CURRENCIES_LIST_API_URL) as response:
                return await response.json()

    async def currency_exists(self, currency: str) -> bool:
        if not self.cached_currencies:
            all_currencies = await self.get_all_currencies()
            self.cached_currencies.update(set(all_currencies))
        return currency in self.cached_currencies


check = CurrencyExistsCheck()
