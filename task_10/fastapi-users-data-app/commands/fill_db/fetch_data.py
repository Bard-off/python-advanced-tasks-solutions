import logging
from typing import Any

import aiohttp

from . import config

log = logging.getLogger(__name__)


async def fetch_api(url: str) -> list[dict[str, Any]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data: list[dict[str, Any]] = await response.json()
            return data


async def fetch_users() -> list[dict[str, Any]]:
    log.info("fetch users")
    data = await fetch_api(url=config.USERS_API)
    log.info("fetched users data: %s", data)
    return data


async def fetch_posts() -> list[dict[str, Any]]:
    log.info("fetch posts")
    data = await fetch_api(url=config.POSTS_API)
    log.info("fetched posts data: %s", data)
    return data
