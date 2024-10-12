import logging
from typing import Any

import requests

import config

log = logging.getLogger(__name__)


def fetch_api(url: str) -> list[dict[str, Any]]:
    return requests.get(url).json()


def fetch_users() -> list[dict[str, Any]]:
    log.info("fetch users")
    data = fetch_api(url=config.USERS_API)
    log.info("fetched users data: %s", data)
    return data


def fetch_posts() -> list[dict[str, Any]]:
    log.info("fetch posts")
    data = fetch_api(url=config.POSTS_API)
    log.info("fetched posts data: %s", data)
    return data
