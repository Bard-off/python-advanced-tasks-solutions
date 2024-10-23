import asyncio
import logging

from commands.fill_db.fetch_data import fetch_posts, fetch_users
from commands.fill_db.prepare_models import (
    prepare_posts_models,
    prepare_users_and_addresses,
)
from core.models import db_helper

log = logging.getLogger(__name__)


async def fill_db() -> None:
    log.info("Fetching api")
    u, p = await asyncio.gather(
        fetch_users(),
        fetch_posts(),
    )
    log.info("Preparing models")
    users, addresses, user_ids_to_users = prepare_users_and_addresses(u)
    posts = prepare_posts_models(p, user_ids_to_users)

    log.info("Saving data")
    async with db_helper.session_factory() as session:
        async with session.begin():
            session.add_all(users)
            session.add_all(addresses)
            session.add_all(posts)
    log.info("Done")
